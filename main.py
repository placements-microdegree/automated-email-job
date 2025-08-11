import sys
import datetime
import os
import pandas as pd
import smtplib
from email.message import EmailMessage

# Log output to both file and console
class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding="utf-8")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = Logger("task_log.txt")
sys.stderr = Logger("task_log.txt")

print("\n---- Task Run:", datetime.datetime.now(), "----")

# Configuration
CSV_PATH = "hremail.csv"
RESUME_PATH = "Dhanush_Raj.pdf"
OUTPUT_CSV = "hremail_updated.csv"
DAILY_LIMIT = 3

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SUBJECT = 'Job Application - Inquiry About Openings'
BODY = """\
Dear HR Team,

I am interested in job openings at your company.
Please find my resume attached for your reference.

Looking forward to your response.

Best regards,
Your Name
"""

# === PRE-CHECKS ===
error_found = False

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    print("❌ ERROR: EMAIL_ADDRESS or EMAIL_PASSWORD environment variables not set.")
    error_found = True

if not os.path.exists(CSV_PATH):
    print(f"❌ ERROR: CSV file not found: {CSV_PATH}")
    error_found = True

if not os.path.exists(RESUME_PATH):
    print(f"❌ ERROR: Resume file not found: {RESUME_PATH}")
    error_found = True

if error_found:
    sys.exit(1)

# === MAIN LOGIC ===
try:
    df = pd.read_csv(CSV_PATH)

    if 'sent' not in df.columns:
        df['sent'] = 0

    unsent = df[df['sent'] == 0].head(DAILY_LIMIT)

    if unsent.empty:
        print("✅ No new emails to send today.")
    else:
        print(f"📤 Sending {len(unsent)} email(s):")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            for idx, row in unsent.iterrows():
                msg = EmailMessage()
                msg['Subject'] = SUBJECT
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = row['email']  # HR email from CSV
                msg['Bcc'] = "habin687@gmail.com"  # Your hidden copy
                msg.set_content(BODY)

                with open(RESUME_PATH, 'rb') as f:
                    resume_data = f.read()
                msg.add_attachment(resume_data, maintype='application', subtype='pdf', filename='Resume.pdf')

                try:
                    smtp.send_message(msg)
                    print(f"✅ Sent to: {row['email']}")
                    with open("email_log.txt", "a", encoding="utf-8") as log:
                        log.write(f"✅ Sent to: {row['email']}\n")
                    df.at[idx, 'sent'] = 10
                except Exception as e:
                    print(f"❌ Failed to send to: {row['email']} – {e}")
                    with open("email_log.txt", "a", encoding="utf-8") as log:
                        log.write(f"❌ Failed to send to: {row['email']} – {e}\n")

        df.to_csv(OUTPUT_CSV, index=False)
        print(f"📁 CSV updated and saved to: {OUTPUT_CSV}")

except Exception as e:
    print(f"❌ SCRIPT CRASHED: {e}")
    sys.exit(1)
