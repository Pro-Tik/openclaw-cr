# config.py
import requests
import sys

# --- Configuration ---
PROJECT_ID = "diu-campus-schedule-cc857"
API_KEY = "AIzaSyBn_0XZrSwcC7dONsNr3M9RiDEKUkpn_S4" 

# ⚠️ PASTE YOUR LONG-LIVED REFRESH TOKEN HERE
REFRESH_TOKEN = "paste_your_refresh_token_here"

# Defaults for your specific class routing
DEFAULT_BATCH = "45"
DEFAULT_SECTION = "I"

def get_fresh_bearer_token():
    """Uses the refresh token to ask Firebase for a brand new 1-hour Bearer token."""
    url = f"https://securetoken.googleapis.com/v1/token?key={API_KEY}"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()['id_token']
    except requests.exceptions.RequestException as e:
        print(f"❌ Critical Error: Failed to refresh token. Did you paste the correct Refresh Token?")
        sys.exit(1)

# Generate a fresh token instantly whenever a script is executed
print("🔄 Getting fresh authorization...")
FRESH_TOKEN = get_fresh_bearer_token()

HEADERS = {
    "Authorization": f"Bearer {FRESH_TOKEN}",
    "Content-Type": "application/json"
}
