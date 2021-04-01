import smtplib
import ssl
import email.encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from .models import User


def sendMail(to, subject, body, file=""):
    me = User.objects.all().values_list('email', flat=True)[0]
    my_password = User.objects.all().values_list('password', flat=True)[0]

    msg = MIMEMultipart('alternative')
    msg['From'] = me
    msg['Subject'] = subject

    msg['To'] = to
    text = body

    msg.attach(MIMEText(text))
    if file != "":
        with open('lab2/upload/' + file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        with open("lab2/upload/" + file.name, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        email.encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file}",
        )
        msg.attach(part)
    else:
        print("No file attached")

    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(me, my_password)

    s.sendmail(me, to, msg.as_string())
    s.quit()
