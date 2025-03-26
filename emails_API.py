import base64
import os
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from certificate_maker import workshop_name,output_dir
from sheet_API import emails, names

# Configuration
Names = names
Emails = emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
WORKSHOP_FOLDER = os.path.join(os.getenv("WORKSHOP_FOLDER"), workshop_name)


output_path = os.path.join(output_dir, f"{workshop_name}_outut.txt")

def gmail_authenticate():
    
    

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def send_email(service, sender, to, subject, message_text, certificate_path):
    with open(output_path, "a", encoding="utf-8") as file:
    
     msg = EmailMessage()
     msg["To"] = to
     msg["From"] = sender
     msg["Subject"] = subject
     msg.set_content(message_text)

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
         file.write(f"Certificate not found:{certificate_path}")

     encoded_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
     body = {"raw": encoded_message}
     try:
         sent = service.users().messages().send(userId="me", body=body).execute()
        
         print(f"✅ Sent to {to}, ID: {sent['id']}")
         file.write(f"✅ Sent to {to}, ID: {sent['id']}\n")
     except Exception as e:
         print("❌ Error sending:", e)
         file.write(f"❌ Error sending: {to}\n")
        


if __name__ == '__main__':
    if os.path.exists('token.json'):
        os.remove('token.json')
    service = gmail_authenticate()

    for i in range(len(Emails)):
        name = Names[i]
        email = Emails[i]
        cert_path = os.path.join(WORKSHOP_FOLDER, f"{name}_certificate.pdf")

        send_email(
            service=service,
            sender=SENDER_EMAIL,
            to=email,
            subject=f'{workshop_name}- Certificate of Completion',
            message_text=f'''
Dear {name},

Thank you for participating in our {workshop_name}!

We hope you found the session insightful and that it helped you enhance your understanding of the topic.

To acknowledge your participation, please find your Certificate of Completion attached to this email.

If you have any feedback or questions, feel free to reach out to us—we’d love to hear from you!

Looking forward to seeing you in future events and workshops.

Best regards,
''',
            certificate_path=cert_path
        )
