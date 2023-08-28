#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import ssl
import time
import os
import csv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


def write_mail(body, recipient, times):
    "writes the mail"
    subject = config.SUBJECT
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


def parse_letter(receiver_record, letter: str) -> str:
    "parses one singular letter based on the fields in receiver record"
    for key, val in receiver_record.items():
        letter = letter.replace(f"_{key}_", val)

    return letter


def parse_letters(receiver_dict, letter):
    "parses many letters based on the fields of receiver file"
    letters = []
    for record in receiver_dict:
        result_letter = parse_letter(record, letter)
        letters.append((result_letter, record["recep-email"]))
    return letters


def main():
    "main fun"
    # with open(config.RECEIPIENTS_MAIL_LIST_FILENAME, 'r', encoding="utf-8") as rec_file:
    #     lines = [line.rstrip() for line in rec_file]
    # list_of_recipients = list(lines)
    # for recipient in list_of_recipients:
    #     write_mail(recipient, 1)

    with open(config.LETTER_FILE, "r", encoding="utf-8") as letter_file:
        letter = letter_file.read()

    with open(config.RECEIVER_MERGE, "r", encoding="utf-8") as receiver_file:
        receiver_dict = csv.DictReader(receiver_file)
        recep_pairs = parse_letters(receiver_dict, letter)

    for tup in recep_pairs:
        write_mail(tup[0], tup[1], 1)


if __name__ == '__main__':
    main()
