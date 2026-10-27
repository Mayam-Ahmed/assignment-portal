import json
import os
import smtplib
from email.message import EmailMessage

with open("report.json", encoding="utf-8") as f:
    r = json.load(f)

s = r["summary"]
lines = [
    f"Repository : {r['repository']}",
    f"Branch     : {r['branch']}",
    f"Commit     : {r['commit_sha']}",
    f"Run ID     : {r['run_id']}",
    f"Time       : {r['timestamp']}",
    f"OVERALL    : {r['overall_status'].upper()}",
    f"Total: {s['total']}  Passed: {s['passed']}  Failed: {s['failed']}",
    "",
    "Individual results:",
]
for t in r["tests"]:
    line = f"  - {t['name']}: {t['result']}"
    if t.get("failure_message"):
        line += f"  ({t['failure_message'][:200]})"
    lines.append(line)

user = os.environ["EMAIL_USERNAME"]
msg = EmailMessage()
msg["Subject"] = f"[{r['overall_status'].upper()}] CI report {r['repository']} @ {r['commit_sha'][:7]}"
msg["From"] = user
msg["To"] = os.environ["EMAIL_TO"]
msg.set_content("\n".join(lines))
msg.add_attachment(json.dumps(r, indent=2).encode(), maintype="application", subtype="json", filename="test-report.json")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(user, os.environ["EMAIL_PASSWORD"])
    smtp.send_message(msg)
print("Email sent")