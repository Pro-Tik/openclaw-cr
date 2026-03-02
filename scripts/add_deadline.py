# add_deadline.py
import requests
import datetime
from config import FIRESTORE_URL, HEADERS, DEFAULT_BATCH, DEFAULT_SECTION

def create_new():
    print("--- Add a New Deadline ---")
    title = input("Title (e.g., DS Lab Evaluation): ")
    date_str = input("Date (YYYY-MM-DD): ")
    task_type = input("Type (Quiz, Assignment, Presentation, Lab Assessment, Lab Final, Lab Report, Lab Project, Lab Task, Project) [Default: Assignment]: ").strip().upper().replace(" ", "_") or "ASSIGNMENT"
    time_str = input("Time (HH:MM) [Default: 23:59]: ") or "23:59"

    payload = {
        "fields": {
            "title": {"stringValue": title},
            "description": {"stringValue": ""},
            "type": {"stringValue": task_type},
            "date": {"stringValue": date_str},
            "time": {"stringValue": time_str},
            "batch": {"stringValue": DEFAULT_BATCH},
            "section": {"stringValue": DEFAULT_SECTION},
            "createdAt": {"integerValue": str(int(datetime.datetime.now().timestamp() * 1000))} 
        }
    }

    print(f"\nPushing '{title}' to database...")
    response = requests.post(FIRESTORE_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        doc_id = response.json().get('name').split('/')[-1]
        print(f"✅ Success! Document ID: {doc_id}")
    elif response.status_code == 401:
         print("❌ Unauthorized: Your Bearer token has expired. Please update config.py.")
    else:
        print(f"❌ Failed. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    create_new()