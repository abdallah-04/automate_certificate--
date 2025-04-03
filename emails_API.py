import base64
import os
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_GMAIL = os.getenv("TOKEN_GMAIL")

def gmail_authenticate():
    creds = None
    if os.path.exists(TOKEN_GMAIL):
        creds = Credentials.from_authorized_user_file(TOKEN_GMAIL, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(os.getenv("CREDENTIALS_PATH"), SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_GMAIL, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def send_email(service, sender, to, subject, message_text, certificate_path,WORKSHOP_NAME):
    LOG_PATH = os.path.join(os.getenv("WORKSHOP_FOLDER"),WORKSHOP_NAME,f"{WORKSHOP_NAME}_output.txt")
    with open(LOG_PATH, "a", encoding="utf-8") as file:
        msg = EmailMessage()
        msg["To"] = to
        msg["From"] = sender
        msg["Subject"] = subject
        msg.add_alternative(message_text, subtype='html')

        if certificate_path and os.path.exists(certificate_path):
            with open(certificate_path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="pdf",
                    filename=os.path.basename(certificate_path)
                )
        else:
            print("Certificate not found:", certificate_path)
            file.write(f"Certificate not found: {certificate_path}\n")
            return

        encoded_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        body = {"raw": encoded_message}
        try:
            sent = service.users().messages().send(userId="me", body=body).execute()
            print(f"✅ Sent to {to}, ID: {sent['id']}")
            file.write(f"✅ Sent to {to}, ID: {sent['id']}\n")
        except Exception as e:
            print("❌ Error sending:", e)
            file.write(f"❌ Error sending to {to}\n")


def send_all_emails(names, emails, WORKSHOP_NAME, output_dir, email_body, sender_name, position):
    service = gmail_authenticate()
    for i in range(len(emails)):
        name = names[i]
        email = emails[i]
        cert_path = os.path.join(output_dir, f"{name}_certificate.pdf")
        subject = f"{WORKSHOP_NAME} - Certificate of Completion"
        custom_body = email_body.format(name=name, WORKSHOP_NAME=WORKSHOP_NAME)

        with open("Email.html", "r", encoding="utf-8") as f:
            signature_html = f.read()

        signature_html = (
            signature_html
            .replace("{sender_name}", sender_name)
            .replace("{position}", position)
        )
        message_text = f"{custom_body}<br><br>{signature_html}"

        send_email(service, os.getenv("SENDER_EMAIL"), email, subject, message_text, cert_path,WORKSHOP_NAME)