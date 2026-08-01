#   AI Gmail Automation

> A private, local AI assistant that reads unread Gmail messages, summarizes them, identifies priorities and action items, and suggests reply drafts.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Ollama](https://img.shields.io/badge/AI-Ollama-black)
![Gmail API](https://img.shields.io/badge/API-Gmail-red?logo=gmail)
![License](https://img.shields.io/badge/Status-Learning%20Project-success)

##  What it does

This automation tool:

- Reads up to 5 unread inbox emails using the Gmail API
- Uses a local Ollama AI model for analysis
- Creates a summary for each message
- Assigns a priority level
- Detects required actions
- Drafts a suggested reply
- Saves everything in `email_report.txt`
- Can run automatically through Windows Task Scheduler

##  Privacy-first design

This project uses a local AI model through Ollama.

- Email analysis happens on the local computer
- No paid AI API is required
- The tool uses Gmail’s read-only permission
- It cannot send, edit, or delete emails

> Never upload `credentials.json`, `token.json`, or `email_report.txt` to GitHub.

##  Technology used

- Python
- Gmail API
- Google OAuth 2.0
- Ollama
- Qwen 3 8B local model
- Windows Task Scheduler

## ⚙️ Setup

### 1. Install Python libraries

```bash
python -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. Install and start Ollama

Download Ollama from:

```text
https://ollama.com
```

Download the recommended local model:

```bash
ollama pull qwen3:8b
```

### 3. Create Gmail credentials

1. Create a Google Cloud project.
2. Enable the Gmail API.
3. Create a Desktop OAuth client.
4. Download the OAuth file.
5. Rename it to `credentials.json`.
6. Place it in this project folder.
7. Add your Gmail address as a test user.
8. Use the `gmail.readonly` permission only.

### 4. Run the automation

```bash
python app.py
```

The first run opens a Google sign-in page. Approve read-only Gmail access.

## Project structure

```text
local-ai-gmail-automation/
│
├── app.py                 # Main automation script
├── credentials.json       # Private Google OAuth credentials
├── token.json             # Private Gmail authorization token
├── email_report.txt       # Generated AI report
├── requirements.txt       # Python dependencies
├── .gitignore             # Protects private files
└── README.md              # Project documentation
```

##  Workflow

```text
Unread Gmail message
        ↓
Gmail API reads email
        ↓
Local Ollama AI analyzes it
        ↓
Summary + priority + action + reply draft
        ↓
email_report.txt is created
```

##  Security notes

The following files must remain private:

```text
credentials.json
token.json
email_report.txt
```

Add them to `.gitignore` before uploading the project to GitHub.

##  Future improvements

- Process only selected Gmail labels
- Add AI-powered category detection
- Create a simple dashboard
- Send notifications for high-priority emails
- Add human approval before sending reply drafts
- Store tasks in Notion, Google Sheets, or a database

##  Credits

Built as a hands-on AI and automation learning project.


