---
name: cr
description: BLC Course Registration & Assignment Tracker. Monitors Daffodil International University eLearn (BLC) for new course assignments and alerts via WhatsApp when new assignments are posted. Use when: (1) Checking for new assignments on BLC, (2) Setting up automated monitoring, (3) Getting WhatsApp alerts for new coursework
---

# CR Skill - BLC Assignment Tracker

This skill monitors the BLC (Daffodil International University eLearn) for new assignments and sends WhatsApp alerts.

## Setup

1. Create `.env` file in `/home/p4b/.openclaw/workspace/skills/public/cr/.env`:
   ```
   BLC_USERNAME=your_username
   BLC_PASSWORD=your_password
   BLC_BASE_URL=https://elearn.daffodilvarsity.edu.bd
   WHATSAPP_TARGET=+8801851407301
   ```

2. Make the script executable:
   ```bash
   chmod +x /home/p4b/.openclaw/workspace/skills/public/cr/scripts/blc_scraper.py
   chmod +x /home/p4b/.openclaw/workspace/skills/public/cr/manage.sh
   ```

## Running the Scraper

To check for new assignments manually, or to add/delete deadlines and announcements:
```bash
cd /home/p4b/.openclaw/workspace/skills/public/cr && ./manage.sh
```

The script will:
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

- Assignments are stored in: `/home/p4b/.openclaw/workspace/skills/public/cr/data/assignments.json`
- The script compares current assignments with stored ones to detect new items
- **Auto-Sync:** Newly detected assignments are also automatically added to the DIU Campus Schedule Firebase app using `scripts/add_deadline.py`
