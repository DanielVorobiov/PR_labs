# skipped your comments for readability
import smtplib
import ssl
import email.encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


me = "vorobiov.daniel@gmail.com"
my_password = r"nvgmhgbvuqcpyofw"
you = "eric199k@gmail.com"

msg = MIMEMultipart('alternative')
msg['Subject'] = "Hello"
msg['From'] = me
msg['To'] = you
text = "Open this"

msg.attach(MIMEText(text))

filename = "r.png"  # In same directory as script

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
email.encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)
msg.attach(part)
# Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
s = smtplib.SMTP_SSL('smtp.gmail.com')
# uncomment if interested in the actual smtp conversation
# s.set_debuglevel(1)
# do the smtp auth; sends ehlo if it hasn't been sent already
s.login(me, my_password)

s.sendmail(me, you, msg.as_string())
s.quit()
