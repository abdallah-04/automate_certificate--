from sheet_API import get_names_and_emails
from certificate_maker import make_certificates
from emails_API import send_all_emails
import os 
def main():
    workshop_name="Backend_Development_Workshop"
    output_dir = os.path.join(os.getenv("BASE_DIR"), f"{workshop_name}")
    names, emails = get_names_and_emails()
    make_certificates(names,output_dir)
    send_all_emails(names, emails,workshop_name,output_dir)

if __name__ == "__main__":
    main()