# add_announcement.py
import requests
import datetime
from config import PROJECT_ID, HEADERS, DEFAULT_BATCH, DEFAULT_SECTION

# The endpoint for announcements is different from deadlines
MESSAGES_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/cr_messages"

def create_announcement():
    print("--- Post a New Announcement ---")
    content = input("Message Content: ")
    
    if not content.strip():
        print("❌ Content cannot be empty. Cancelled.")
        return

    # Defaulting to your details from the browser logs
    author_name = input("Author Name [Default: Pratik]: ").strip() or "Pratik"
    author_id = "T5k61xmmpCbH6uSR3fcpx58pjsq2" 

    payload = {
        "fields": {
            "content": {"stringValue": content},
            "batch": {"stringValue": DEFAULT_BATCH},
            "section": {"stringValue": DEFAULT_SECTION},
            "authorId": {"stringValue": author_id},
            "authorName": {"stringValue": author_name},
            "createdAt": {"integerValue": str(int(datetime.datetime.now().timestamp() * 1000))} 
        }
    }

    print(f"\nBroadcasting to {DEFAULT_BATCH}-{DEFAULT_SECTION}...")
    response = requests.post(MESSAGES_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        doc_id = response.json().get('name').split('/')[-1]
        print(f"✅ Announcement live! Document ID: {doc_id}")
    elif response.status_code == 401:
         print("❌ Unauthorized: Your Bearer token has expired. Please update config.py.")
    else:
        print(f"❌ Failed. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    create_announcement()