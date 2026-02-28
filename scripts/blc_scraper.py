import os
import requests
from bs4 import BeautifulSoup
import json
import re
import calendar
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- Configuration ---
BASE_URL = os.getenv("BLC_BASE_URL", "https://elearn.daffodilvarsity.edu.bd")
USERNAME = os.getenv("BLC_USERNAME")
PASSWORD = os.getenv("BLC_PASSWORD")
DATA_FILE = "./.openclaw/workspace/skills/public/cr/data/assignments.json"

class BLCScraper:
    def __init__(self):
        self.session = requests.Session()
        self.sesskey = None

    def login(self):
        print("--- Step 1: Authenticating with BLC ---")
        if not USERNAME or not PASSWORD:
            print("Error: Missing BLC_USERNAME or BLC_PASSWORD in .env file")
            return False
        try:
            # 1. Get Login Token
            login_page = self.session.get(f"{BASE_URL}/login/index.php")
            soup = BeautifulSoup(login_page.text, 'html.parser')
            login_token = soup.find('input', {'name': 'logintoken'})['value']
            
            # 2. Post Credentials
            payload = {'username': USERNAME, 'password': PASSWORD, 'logintoken': login_token}
            response = self.session.post(f"{BASE_URL}/login/index.php", data=payload)
            
            if "login/index.php" in response.url:
                print("Error: Login failed. Check credentials.")
                return False
            
            # 3. Extract Sesskey
            match = re.search(r'"sesskey":"([^"]+)"', response.text)
            if not match:
                print("Error: Could not find sesskey.")
                return False
            
            self.sesskey = match.group(1)
            print(f"Login Successful! Sesskey: {self.sesskey}")
            return True
        except Exception as e:
            print(f"Connection Error: {e}")
            return False

    def get_courses(self):
        print("\n--- Current Spring 2026 Courses ---")
        url = f"{BASE_URL}/lib/ajax/service.php?sesskey={self.sesskey}&info=core_course_get_recent_courses"
        payload = [{"index": 0, "methodname": "core_course_get_recent_courses", "args": {"userid": 0}}]
        res = self.session.post(url, json=payload).json()
        
        clean_courses = []
        
        # Check if response is valid
        if isinstance(res, list) and not res[0].get('error'):
            print(f"{'ID':<8} | {'SHORTNAME':<15} | {'FULL NAME'}")
            print("-" * 80)
            for course in res[0]['data']:
                # Only grab the current semester
                if "Spring 2026" in course.get('coursecategory', ''):
                    c = {
                        "id": course['id'],
                        "name": course['fullname'],
                        "short": course['shortname'],
                        "progress": f"{course.get('progress', 0)}%"
                    }
                    clean_courses.append(c)
                    print(f"{c['id']:<8} | {c['short']:<15} | {c['name']}")
        else:
            print("Failed to retrieve courses.")
        return clean_courses

    def get_tasks_for_month(self, year=None, month=None):
        # Default to current month/year if not specified
        if year is None or month is None:
            now = datetime.now()
            year, month = now.year, now.month
        
        print(f"\n--- Assignments for {calendar.month_name[month]} {year} ---")
        
        # Calculate the exact timestamp for the 1st of the month and the last minute of the last day
        first_day = datetime(year, month, 1)
        last_day_num = calendar.monthrange(year, month)[1]
        last_day = datetime(year, month, last_day_num, 23, 59, 59)
        
        url = f"{BASE_URL}/lib/ajax/service.php?sesskey={self.sesskey}&info=core_calendar_get_action_events_by_timesort"
        payload = [{
            "index": 0,
            "methodname": "core_calendar_get_action_events_by_timesort",
            "args": {
                "limitnum": 50,  # Fetch up to 50 tasks for the month
                "timesortfrom": int(first_day.timestamp()),
                "timesortto": int(last_day.timestamp()),
                "userid": 0
            }
        }]
        
        res = self.session.post(url, json=payload).json()
        
        clean_tasks = []
        
        if isinstance(res, list) and 'events' in res[0].get('data', {}):
            events = res[0]['data']['events']
            
            if not events:
                print("No tasks or deadlines found for this month! 🎉")
                return clean_tasks
            
            print(f"{'DEADLINE':<30} | {'COURSE':<15} | {'TASK'}")
            print("-" * 90)
            
            for event in events:
                # Strip out any HTML tags (like links) from the deadline text
                raw_time = event.get('formattedtime', 'Unknown Time')
                clean_time = BeautifulSoup(raw_time, "html.parser").text
                
                t = {
                    "name": event['name'],
                    "course": event['course']['shortname'],
                    "deadline": clean_time,
                    "url": event['url']
                }
                clean_tasks.append(t)
                print(f"{t['deadline']:<30} | {t['course']:<15} | {t['name']}")
        else:
            print("Error retrieving monthly task data.")
        
        return clean_tasks

def fetch_blc_data():
    """Wrapper function designed to be called by an OpenClaw Skill.
    Returns the scraped data as a Python dictionary.
    """
    scraper = BLCScraper()
    
    if scraper.login():
        courses = scraper.get_courses()
        tasks = scraper.get_tasks_for_month()
        
        return {
            "courses": courses,
            "tasks": tasks,
            "timestamp": datetime.now().isoformat()
        }
    
    return {"error": "Login failed"}

def load_previous_assignments():
    """Load previously saved assignments from file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_assignments(assignments):
    """Save assignments to file"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(assignments, f, indent=2)

def find_new_assignments(current_tasks, previous_tasks):
    """Find tasks that weren't in the previous list"""
    previous_titles = {t['name'] for t in previous_tasks}
    new = [t for t in current_tasks if t['name'] not in previous_titles]
    return new

def send_whatsapp_alert(new_tasks):
    """Send WhatsApp alert for new tasks without using AI"""
    if not new_tasks:
        return
    
    whatsapp_script = "/home/procloud/.openclaw/workspace/skills/public/whatsapp-sender/scripts/send_message.sh"
    target = os.getenv("WHATSAPP_TARGET", "+8801851407301")
    
    for task in new_tasks:
        message = f"🚨 *New Assignment!*\n\n*Course:* {task['course']}\n*Task:* {task['name']}\n*Due:* {task['deadline']}"
        cmd = f"bash {whatsapp_script} '{target}' '{message}'"
        os.system(cmd)
        print(f"  📱 WhatsApp alert sent for: {task['name']}")

def main():
    scraper = BLCScraper()
    
    if not scraper.login():
        print("[FAIL] Login failed")
        return
    
    courses = scraper.get_courses()
    current_tasks = scraper.get_tasks_for_month()
    
    # Load previous tasks
    previous_tasks = load_previous_assignments()
    
    # Find new tasks
    new_tasks = find_new_assignments(current_tasks, previous_tasks)
    
    if new_tasks:
        print(f"\n🚨 NEW ASSIGNMENTS FOUND: {len(new_tasks)}")
        for t in new_tasks:
            print(f"  ⚠️ {t['course']}: {t['name']} - Due: {t['deadline']}")
        
        # Send WhatsApp alerts (no AI tokens used)
        send_whatsapp_alert(new_tasks)
    else:
        print("\n✅ No new assignments found")
    
    # Save current tasks
    save_assignments(current_tasks)
    
    print("\n[SUCCESS] Dashboard data extracted successfully.")
    
    # Return new tasks for alerting
    return new_tasks

if __name__ == "__main__":
    main()
