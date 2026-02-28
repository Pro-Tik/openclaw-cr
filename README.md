# OpenClaw CR: BLC Portal Skill

A custom skill for OpenClaw AI agents that securely authenticates with the **Daffodil International University (DIU) BLC portal (Moodle)** to fetch current semester courses and upcoming assignment deadlines.

Designed specifically for **Class Representatives (CRs)** and students to automate deadline tracking and feed real-time university data directly into their personal AI assistants.

---

## Features

### Automated Authentication

Securely manages Moodle session tokens (`sesskey`) behind the scenes.

### Course Filtering

Automatically filters out past semesters to only display current, active courses (e.g., *Spring 2026*).

### Smart Timeline

Bypasses restricted calendar endpoints to fetch all upcoming assignments and deadlines for the current month.

### AI-Ready Format

Pre-formats the scraped data into token-efficient strings and structured JSON, preventing LLM hallucinations.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Pro-Tik/openclaw-cr.git
cd openclaw-cr
```

### 2. Set up your virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install requests beautifulsoup4 python-dotenv
```

---

## Configuration

Security is a priority. **Never hardcode your university password.**

Create a `.env` file in the root of the project to store your credentials:

```bash
touch .env
```

Add the following variables to your `.env` file:

```env
BLC_BASE_URL="https://elearn.daffodilvarsity.edu.bd"
BLC_USERNAME="your_student_id_or_username"
BLC_PASSWORD="your_secure_password"
```

> ⚠️ Ensure `.env` is listed in your `.gitignore` to prevent leaking your credentials to GitHub.

---

## Usage

### Standalone (Terminal)

Run the scraper directly from your terminal to generate a local `blc_data.json` dashboard file:

```bash
python scripts/blc_scraper.py
```

---

### As an OpenClaw Skill

To integrate this with your OpenClaw agent:

1. Ensure the skill is registered in your agent's skill directory.
2. Start your OpenClaw agent.

You can then ask natural language queries like:

* "Agent, what assignments do I have due for Data Structures this month?"
* "Can you check my BLC portal and list my current courses?"

The agent will trigger `check_university_deadlines()`, scrape the portal in real-time, and format the response for you.

---

## Built With

* **Python 3**
* **Requests** — HTTP sessions and AJAX calls
* **BeautifulSoup4** — HTML parsing and token extraction
* **python-dotenv** — Secure environment variable management
