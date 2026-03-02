import requests
from config import HEADERS, PROJECT_ID

MESSAGES_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/cr_messages"

def remove_item():
    print("--- Delete an Announcement ---")
    doc_id = input("Enter the Document ID to delete: ")
    
    if not doc_id:
        print("Cancelled.")
        return

    delete_url = f"{MESSAGES_URL}/{doc_id}"
    print(f"\nDeleting {doc_id}...")
    
    response = requests.delete(delete_url, headers=HEADERS)

    if response.status_code == 200:
        print("✅ Successfully deleted!")
    elif response.status_code == 401:
         print("❌ Unauthorized: Your Bearer token has expired. Please update config.py.")
    else:
        print(f"❌ Failed to delete. Status: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    remove_item()
