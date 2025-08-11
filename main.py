import sys
import datetime
import os
import pandas as pd
import smtplib
from email.message import EmailMessage

# Log output to file
log_file = open("task_log.txt", "a", encoding="utf-8")
sys.stdout = log_file
sys.stderr = log_file

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

# Load CSV
df = pd.read_csv(CSV_PATH)

# Add 'sent' column if missing
if 'sent' not in df.columns:
    df['sent'] = 0

# Get unsent emails
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
            msg['Bcc'] = "habin687@gmail.com"  # Your email gets hidden copy
            msg.set_content(BODY)

            # Attach resume
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

    # Save updated CSV
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"📁 CSV updated and saved to: {OUTPUT_CSV}")
