### **Project Overview: Automated Certificate Generation and Emailing System**  

This project automates the process of generating certificates for workshop participants and emailing them their certificates. The system consists of three main components:  

1. **Data Extraction (sheet_API.py)**  
2. **Certificate Generation (certificate_maker.py)**  
3. **Email Dispatching (emails_API.py)**  

Each file is responsible for a distinct task in the automation workflow.  

---

## **1. sheet_API.py (Google Sheets API Integration)**  
**Purpose:**  
Fetches participant names and emails from a Google Sheet.  

**Key Functionalities:**  
- Authenticates with the Google Sheets API using OAuth 2.0.  
- Reads participant names and emails from a specified spreadsheet.  
- Returns two lists: `names` and `emails`, which are used in later scripts.  

**How It Works:**  
- Uses `credentials.json` and `token.json` for authentication.  
- Reads the spreadsheet ID from an environment variable (`SPREADSHEET_ID`).  
- Extracts names and emails from the range `B2:C` of the sheet named `"Form Responses 1"`.  

---

## **2. certificate_maker.py (Certificate Generation Using PIL)**  
**Purpose:**  
Generates certificates for each participant by overlaying their names on a predefined certificate template.  

**Key Functionalities:**  
- Loads a certificate template image.  
- Draws the participant’s name at a specific position using PIL (`ImageDraw`).  
- Saves the generated certificates as PDF files in a workshop-specific folder.  

**How It Works:**  
- Reads the workshop name (`Backend_Development_Workshop`).  
- Reads names from `sheet_API.py`.  
- Fetches the certificate template path from an environment variable (`certificate_path`).  
- Uses a font specified by `FONT_PATH` to write the name.  
- Saves each certificate as a PDF file in the workshop directory.  

---

## **3. emails_API.py (Automated Email Sending via Gmail API)**  
**Purpose:**  
Emails the generated certificates to the respective participants.  

**Key Functionalities:**  
- Authenticates with Gmail API using OAuth 2.0.  
- Composes an email with the certificate attached.  
- Sends the email to each participant.  

**How It Works:**  
- Reads participant names and emails from `sheet_API.py`.  
- Reads certificates from `certificate_maker.py`.  
- Authenticates with Gmail API (`gmail_authenticate`).  
- Composes an email with a personalized message.  
- Attaches the participant’s certificate and sends the email.  
- Logs successful and failed emails to an output text file (`workshop_name_output.txt`).  

---

## **4. credentials.json (Google API Credentials File)**  
**Purpose:**  
Stores OAuth 2.0 credentials for accessing Google Sheets and Gmail APIs.  

**Key Components:**  
- `client_id`  
- `client_secret`  
- `auth_uri`, `token_uri`  
- Redirect URIs (for authentication flow)  

---

## **Execution Flow**  
1. `sheet_API.py` extracts names and emails from Google Sheets.  
2. `certificate_maker.py` generates certificates for each participant.  
3. `emails_API.py` sends the certificates via email.  

This system automates the entire process of issuing digital certificates, making it efficient and scalable.