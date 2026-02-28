# OpenClaw Skill: BLC Portal (DIU Moodle)

This repository provides an installable **OpenClaw Skill** that enables an OpenClaw agent to securely authenticate with the Daffodil International University (DIU) BLC portal (Moodle) and fetch:

* Current active semester courses
* Upcoming assignment deadlines (current month)
* Structured, AI-ready academic data

The skill is designed so an OpenClaw agent can be instructed to fetch and install it directly from this repository.

---

## Repository

```
https://github.com/Pro-Tik/openclaw-cr
```

An OpenClaw agent can be instructed with:

> "Go to this repository and install the BLC Portal skill: [https://github.com/Pro-Tik/openclaw-cr](https://github.com/Pro-Tik/openclaw-cr)"

---

## What This Skill Does

### Secure Authentication

* Logs into DIU BLC (Moodle)
* Manages session cookies and `sesskey` automatically
* Avoids exposing credentials in source code

### Active Course Detection

* Filters out past semesters
* Returns only currently active courses (e.g., Spring 2026)

### Assignment & Deadline Extraction

* Fetches upcoming assignments for the current month
* Bypasses restricted calendar endpoints when necessary
* Produces structured JSON output

### LLM-Optimized Output

* Token-efficient formatting
* Clean structured data
* Reduces hallucination risk by grounding responses in live portal data

---

## Installation (Manual Setup)

If installing manually instead of through an OpenClaw agent:

### 1. Clone the repository

```bash
git clone https://github.com/Pro-Tik/openclaw-cr.git
cd openclaw-cr
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install requests beautifulsoup4 python-dotenv
```

---

## Configuration

Security is mandatory. Never hardcode credentials.

Create a `.env` file in the project root:

```bash
touch .env
```

Add:

```env
BLC_BASE_URL="https://elearn.daffodilvarsity.edu.bd"
BLC_USERNAME="your_student_id_or_username"
BLC_PASSWORD="your_secure_password"
```

Ensure `.env` is listed in `.gitignore`.

---

## Using as an OpenClaw Skill

1. Place this repository inside your OpenClaw agent's skills directory
   OR
2. Instruct your OpenClaw agent to fetch and register this repository as a skill

Once registered, the agent can trigger the internal function:

```
check_university_deadlines()
```

Example natural language prompts:

* "Check my BLC portal and list my current courses."
* "What assignments are due this month?"
* "Do I have anything due for Data Structures this week?"

The agent will:

1. Authenticate with BLC
2. Scrape live academic data
3. Format structured output
4. Return grounded results

---

## Standalone Usage (Optional)

To generate a local dashboard file:

```bash
python scripts/blc_scraper.py
```

This will create:

```
blc_data.json
```

---

## Built With

* Python 3
* requests
* beautifulsoup4
* python-dotenv

---

## Purpose

This skill allows OpenClaw agents to act as real-time academic assistants for DIU students and Class Representatives by directly integrating university portal data into agent workflows.
