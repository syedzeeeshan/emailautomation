import base64
import json
import os.path
import urllib.error
import urllib.request

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
MODEL = "qwen3:4b"
MAX_EMAILS = 5


def get_gmail_service():
    credentials = None

    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            credentials = flow.run_local_server(port=0)

        with open("token.json", "w", encoding="utf-8") as token_file:
            token_file.write(credentials.to_json())

    return build("gmail", "v1", credentials=credentials)


def get_message_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data", "")
                return base64.urlsafe_b64decode(data + "==").decode(
                    "utf-8",
                    errors="replace"
                )

            body = get_message_body(part)
            if body:
                return body

    data = payload.get("body", {}).get("data", "")
    if data:
        return base64.urlsafe_b64decode(data + "==").decode(
            "utf-8",
            errors="replace"
        )

    return "(No readable plain-text message body found.)"


def get_unread_emails(service):
    results = service.users().messages().list(
        userId="me",
        q="is:unread in:inbox",
        maxResults=MAX_EMAILS
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for message in messages:
        full_message = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        headers = full_message["payload"].get("headers", {})
        header_map = {
            header["name"].lower(): header["value"]
            for header in headers
        }

        emails.append({
            "from": header_map.get("from", "Unknown sender"),
            "subject": header_map.get("subject", "(No subject)"),
            "body": get_message_body(full_message["payload"])
        })

    return emails


def analyze_email_with_ai(email):
    prompt = f"""
You are an email assistant.

Analyze this email using exactly these headings:

Summary:
Priority:
Action:
Suggested reply:

Sender: {email["from"]}
Subject: {email["subject"]}
Body: {email["body"]}
"""

    data = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }).encode("utf-8")

    request = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(request, timeout=300) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result["message"]["content"]


service = get_gmail_service()
emails = get_unread_emails(service)

report = "LOCAL AI GMAIL REPORT\n"
report += "=" * 40 + "\n\n"

if not emails:
    report += "No unread inbox emails found.\n"

for email in emails:
    print(f"Analyzing: {email['subject']}")
    analysis = analyze_email_with_ai(email)

    report += f"From: {email['from']}\n"
    report += f"Subject: {email['subject']}\n\n"
    report += analysis
    report += "\n" + "-" * 40 + "\n\n"

with open("email_report.txt", "w", encoding="utf-8") as report_file:
    report_file.write(report)

print("Gmail AI automation completed.")
print("Your report was saved as email_report.txt")