---
name: cr
description: BLC Course Registration & DIU Campus Schedule Manager. A unified skill that monitors Daffodil International University eLearn (BLC) for new assignments and manages a Firebase-backed campus schedule (deadlines and announcements).
---

# CR Skill - BLC Assignment Tracker & Schedule Manager

This skill combines two powerful systems into one OpenClaw integration:
1. **BLC Scraper**: Monitors Daffodil International University eLearn for new assignments, alerts via WhatsApp, and automatically synchronizes them to your campus schedule database.
2. **Campus Schedule Manager**: Manages your Firebase-backed Campus Schedule by fetching, adding, or deleting deadlines and announcements.

## Setup

### 1. BLC Authentication (.env)
Create an `.env` file in the root directory (`/home/p4b/.openclaw/workspace/skills/public/cr/.env`):
```env
BLC_USERNAME=your_username
BLC_PASSWORD=your_password
BLC_BASE_URL=https://elearn.daffodilvarsity.edu.bd
WHATSAPP_TARGET=+8801851407301
```

### 2. Firebase Database Integration (config.py)
Create a `config.py` file inside the scripts directory (`/home/p4b/.openclaw/workspace/skills/public/cr/scripts/config.py`):
```python
PROJECT_ID = "diu-campus-schedule-cc857"
BEARER_TOKEN = "your_fresh_firebase_bearer_token"
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/deadlines"
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}", "Content-Type": "application/json"}
DEFAULT_BATCH = "45"
DEFAULT_SECTION = "I"
```
*(Remember to update the BEARER_TOKEN when it expires!)*

### 3. Make the Scripts Executable:
   ```bash
   chmod +x /home/p4b/.openclaw/workspace/skills/public/cr/scripts/blc_scraper.py
   chmod +x /home/p4b/.openclaw/workspace/skills/public/cr/manage.sh
   ```

## Running the Systems

You can run both systems through the interactive shell manager:
```bash
cd /home/p4b/.openclaw/workspace/skills/public/cr && ./manage.sh
```

### System 1: The BLC Scraper
When checking BLC for new assignments, the script will:
1. Login to your BLC account
2. Fetch current courses and tasks
3. Compare with previously recorded assignments in `data/assignments.json`
4. Send a WhatsApp alert for any new items found.
5. **Auto-Sync:** Push the new assignments directly into your Campus Schedule Database!

### System 2: The Campus Schedule Manager
When checking the schedule, you can manage your database manually:
- View current deadlines from Firebase
- Add new announcements or deadlines
- Delete obsolete announcements by their Document ID
1. Login to BLC
2. Fetch current courses
3. Get assignments
4. Compare with previously recorded assignments
5. Return new assignments found

## Automated Monitoring

To set up automatic checking (e.g., every hour), add a cron job:
```bash
crontab -e
# Add: 0 * * * * cd /home/p4b/.openclaw/workspace/skills/public/cr && python3 scripts/blc_scraper.py >> /tmp/blc_scraper.log 2>&1
```

## WhatsApp Alert Integration

When new assignments are found, send alerts using the WhatsApp sender script:
```bash
bash /home/p4b/.openclaw/workspace/skills/public/whatsapp-sender/scripts/send_message.sh 'TARGET_NUMBER' 'Assignment: TITLE | Course: COURSE | Due: DEADLINE'
```

## Data Storage & Firebase Sync

- Local assignments are cached in: `/home/p4b/.openclaw/workspace/skills/public/cr/data/assignments.json`
- The BLC scraper compares current assignments with stored ones to detect new items
- **Firebase Auto-Sync:** Newly detected BLC assignments are automatically pushed to the DIU Campus Schedule app using the `scripts/add_deadline.py` logic.
