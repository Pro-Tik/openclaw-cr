# fetch_deadlines.py
import requests
from config import FIRESTORE_URL, HEADERS

def get_all():
    print("Fetching active deadlines...\n")
    try:
        response = requests.get(FIRESTORE_URL, headers=HEADERS)
        
        if response.status_code == 401:
            print("❌ Unauthorized: Your Bearer token has expired. Please update config.py.")
            return

        response.raise_for_status()
        documents = response.json().get('documents', [])
        
        if not documents:
            print("No deadlines found.")
            return

        for doc in documents:
            fields = doc.get('fields', {})
            doc_id = doc.get('name', '').split('/')[-1]
            title = fields.get('title', {}).get('stringValue', 'Untitled')
            due_date = fields.get('date', {}).get('stringValue', 'No Date')
            
            print(f"📌 {title}")
            print(f"   Due: {due_date}")
            print(f"   ID:  {doc_id}")
            print("-" * 30)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_all()