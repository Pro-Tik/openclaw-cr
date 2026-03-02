# fetch_announcements.py
import requests
from config import PROJECT_ID, HEADERS

# Your specific Firebase User UID
MY_USER_ID = "T5k61xmmpCbH6uSR3fcpx58pjsq2"

MESSAGES_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/cr_messages"

def get_my_announcements():
    print("Fetching your active announcements...\n")
    try:
        response = requests.get(MESSAGES_URL, headers=HEADERS)
        
        if response.status_code == 401:
            print("❌ Unauthorized: Your Bearer token has expired. Please update config.py.")
            return

        response.raise_for_status()
        documents = response.json().get('documents', [])
        
        if not documents:
            print("No announcements found in the database.")
            return

        found_mine = False
        for doc in documents:
            fields = doc.get('fields', {})
            
            # Check who authored this document
            author_id = fields.get('authorId', {}).get('stringValue', '')
            
            # 🛑 THE FILTER: Only print if the author ID matches YOUR account
            if author_id == MY_USER_ID:
                found_mine = True
                doc_id = doc.get('name', '').split('/')[-1]
                
                content = fields.get('content', {}).get('stringValue', 'No Content')
                batch = fields.get('batch', {}).get('stringValue', 'Unknown')
                section = fields.get('section', {}).get('stringValue', 'Unknown')
                
                print(f"📢 {content}")
                print(f"   Target: Batch {batch}, Section {section}")
                print(f"   ID: {doc_id}")
                print("-" * 40)

        if not found_mine:
            print("You don't have any active announcements right now.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_my_announcements()