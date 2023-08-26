import email
import smtplib
import ssl
import time
import config
import os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def write_mail(recipient, times):
    subject = config.SUBJECT
    body = config.EMAIL_BODY
    sender_email = config.SENDER_EMAIL
    receiver_email = recipient
    login = os.environ.get("hsma_username")
    password = os.environ.get("hsma_password")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # filename = config.ATTACHMENT_FILENAME  # In same directory as script

    # Open PDF file in binary mode
    # with open(filename, "rb") as attachment:
    #     # Add file as application/octet-stream
    #     # Email client can usually download this automatically as attachment
    #     part = MIMEBase("application", "octet-stream")
    #     part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    # encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    # part.add_header(
    # "Content-Disposition",
    # f"attachment; filename= {filename}",
    # )

    # Add attachment to message and convert message to string
    # message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("mail.hs-mannheim.de", 465, context=context) as server:
        server.login(login, password)
        for i in range(times):
            time.sleep(10)
            server.sendmail(sender_email, receiver_email, text)


def main():
    with open(config.RECEIPIENTS_MAIL_LIST_FILENAME, 'r') as f:
        lines = [line.rstrip() for line in f]
    list_of_recipients = list(lines)
    for recipient in list_of_recipients:
        write_mail(recipient, 1)


if __name__ == '__main__':
    main()
