from .models import User
import smtplib
import imaplib
import email
import traceback


from_email = User.objects.all().values_list('email', flat=True)[0]
from_pwd = User.objects.all().values_list('password', flat=True)[0]
SMTP_SERVER = "imap.gmail.com"

mail = imaplib.IMAP4_SSL(SMTP_SERVER)
mail.login(from_email, from_pwd)
mail.select('inbox')

data = mail.search(None, 'ALL')
mail_ids = data[1]
id_list = mail_ids[0].split()
first_email_id = int(id_list[0])
latest_email_id = int(id_list[-1])


email_from_list = []
email_subject_list = []
email_body_list = []


def get_subject():
    _email_subject_list = []
    for i in range(latest_email_id, latest_email_id-4, -1):
        data = mail.fetch(str(i), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1], 'utf-8'))
                email_subject = msg['subject']
                _email_subject_list.append(email_subject)
    return _email_subject_list


def get_from():
    _email_from_list = []
    for i in range(latest_email_id, latest_email_id-4, -1):
        data = mail.fetch(str(i), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1], 'utf-8'))
                email_from = msg['from']
                if '<' in email_from:
                    email_from = email_from[:email_from.index("<")]
                _email_from_list.append(email_from)
    return _email_from_list


def get_body():

    _email_body_list = []
    for i in range(latest_email_id, latest_email_id-4, -1):
        data = mail.fetch(str(i), '(RFC822)')
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1], 'utf-8'))
                for part in msg.walk():
                    # each part is a either non-multipart, or another multipart message
                    # that contains further parts... Message is organized like a tree
                    if part.get_content_type() == 'text/plain':
                        # prints the raw text
                        email_body = part.get_payload(decode=True)
                        body = email_body.decode('utf-8')
                        if len(body) > 300:
                            body = body[0:300] + "..."
                        _email_body_list.append(body)

    return _email_body_list


email_from_list = get_from()
email_subject_list = get_subject()
email_body_list = get_body()
