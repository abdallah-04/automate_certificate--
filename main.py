from sheet_API import get_names_and_emails
from certificate_maker import make_certificates
from emails_API import send_all_emails
import os 
from dotenv import load_dotenv
import app 

load_dotenv()


def main():
    workshop_name = os.getenv("WORKSHOP_NAME")
    certificate_type=os.getenv("CERT_TYPE")
    certificate_path=os.getenv("certificate_path")
    output_dir = os.getenv("BASE_DIR")
    email_body = os.getenv("EMAIL_BODY")
    sender_name = os.getenv("SENDER_NAME")
    position = os.getenv("POSITION")
    os.makedirs(output_dir, exist_ok=True)
    names, emails = get_names_and_emails()
    make_certificates(names,output_dir,certificate_type,certificate_path)
    send_all_emails(names, emails, workshop_name, output_dir, email_body, sender_name, position)

if __name__ == "__main__":
    app.run_gui()
     