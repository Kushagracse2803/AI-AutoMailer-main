import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from dotenv import load_dotenv

load_dotenv()


def send_email(
    recipient_email,
    subject,
    body,
    resume_path="Kushagra_AI_ML.pdf"
):

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()

    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(
        MIMEText(body, "plain")
    )

    with open(resume_path, "rb") as f:

        attachment = MIMEApplication(
            f.read(),
            _subtype="pdf"
        )

        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename="Kushagra_AI_ML.pdf"
        )

        msg.attach(attachment)

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        sender_email,
        sender_password
    )

    server.send_message(msg)

    server.quit()

    return True