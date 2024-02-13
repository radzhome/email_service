"""
This script is used to test the email server setup. It sends an email to itself.
"""
import smtplib
import logging

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

GOOGLE_EMAIL = settings.GOOGLE_EMAIL
GOOGLE_EMAIL_APP_PASSWORD = settings.GOOGLE_EMAIL_APP_PASSWORD


def send_gmail(subject, message, send_to, reply_to, sent_from=GOOGLE_EMAIL, app_password=GOOGLE_EMAIL_APP_PASSWORD):
    """
    Send an email using the Gmail SMTP server
    :param subject: The subject of the email
    :param message: The message body of the email
    :param send_to: list, of email addresses to send the email to
    :param reply_to: The reply-to email address
    :param sent_from: The email address to send the email from
    :param app_password: The app password to use to authenticate with the Gmail SMTP server
    """
    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(sent_from, app_password)

    # Join the list of recipients into a comma-separated string if applicable
    send_to = ', '.join(send_to)  if isinstance(send_to, list) else send_to

    # Create a MIMEText object for the email content
    msg = MIMEMultipart()
    msg['From'] = sent_from
    msg['To'] = send_to
    msg['Subject'] = subject
    msg['Reply-To'] = reply_to

    # Attach the message body to the email
    msg.attach(MIMEText(message, 'plain'))

    # Convert the MIMEMultipart object to a string
    email_text = msg.as_string()

    smtpserver.sendmail(sent_from, send_to, email_text)

    smtpserver.close()
    logging.info("send_gmail email sent to %s", send_to)
    return True