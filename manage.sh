#!/bin/bash

# Activate virtual environment if it exists (optional but recommended)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

while true; do
    echo ""
    echo "=== DIU Campus Schedule Manager ==="
    echo "1. Add Deadline"
    echo "2. Add Announcement"
    echo "3. Fetch Deadlines"
    echo "4. Fetch Announcements"
    echo "5. Delete Deadline"
    echo "6. Delete Announcement"
    echo "7. Check BLC for New Assignments (Scraper)"
    echo "8. Exit"
    echo "==================================="
    read -p "Choose an option (1-8): " opt

    case $opt in
        1) python3 scripts/add_deadline.py ;;
        2) python3 scripts/add_announcement.py ;;
        3) python3 scripts/fetch_deadlines.py ;;
        4) python3 scripts/fetch_announcements.py ;;
        5) 
           echo ""
           echo "--- Current Deadlines ---"
           python3 scripts/fetch_deadlines.py
           echo ""
           python3 scripts/delete_deadline.py
           ;;
        6) 
           echo ""
           echo "--- Current Announcements ---"
           python3 scripts/fetch_announcements.py
           echo ""
           python3 scripts/delete_announcement.py
           ;;
        7)
           echo ""
           echo "--- Checking BLC ---"
           python3 scripts/blc_scraper.py
           ;;
        8) 
           echo "Exiting..."
           break 
           ;;
        *) echo "Invalid option, please try again." ;;
    esac
done
