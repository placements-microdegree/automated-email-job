# Automated Email Job for HR Outreach

This Python script automates sending job application emails with a resume attachment to HR contacts listed in a CSV file. It is scheduled to run **twice a day** at **9:00 AM and 9:00 PM IST** using a Render Cron Job.

---

## 🔧 How It Works
- Reads emails from `hremail.csv`
- Sends up to 3 unsent emails per run
- Attaches `Dhanush_Raj.pdf` as the resume
- Logs activity to `task_log.txt` and `email_log.txt`
- Updates sent status in `hremail_updated.csv`

---

## 📁 Files
| File | Description |
|------|-------------|
| `send_emails.py` | Main Python script |
| `hremail.csv` | Input list of HR emails |
| `Dhanush_Raj.pdf` | Resume attachment |
| `requirements.txt` | Python dependencies |
| `task_log.txt` | Run logs (auto-generated) |
| `email_log.txt` | Email delivery logs (auto-generated) |

---

## ⚙️ Environment Variables (on Render)
| Key | Value |
|-----|-------|
| `EMAIL_ADDRESS` | your_email@gmail.com |
| `EMAIL_PASSWORD` | app_password_here |

---

## 🕒 Schedule on Render
Runs at:
- 9:00 AM IST → `30 3 * * *` UTC
- 9:00 PM IST → `30 15 * * *` UTC

---

## 📦 Setup (if running locally)
```bash
pip install -r requirements.txt
python send_emails.py
