import base64
import pickle
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


class Mailer:
    @staticmethod
    def __get_creds(token_file):
        creds = None

        if os.path.exists(token_file):
            with open(token_file, "rb") as f:
                creds = pickle.load(f)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            if not creds or not creds.valid:
                raise RuntimeError("Invalid gmail credentials")
            with open(token_file, "wb") as f:
                pickle.dump(creds, f)

        return creds

    def __init__(self, token_file, src_address, dst_address):
        self.creds = Mailer.__get_creds(token_file)
        self.src_address = src_address
        self.dst_address = dst_address

    def send(self, subject, body):
        message = MIMEMultipart()
        message["to"] = self.dst_address
        message["from"] = self.src_address
        message["subject"] = subject

        message.attach(MIMEText(f"{subject} is attached."))

        attachment = MIMEText(body, "html")
        attachment.add_header(
            "Content-Disposition", "attachment", filename=f"{subject}.html"
        )
        message.attach(attachment)

        mail = {
            "raw": base64.urlsafe_b64encode(message.as_string().encode("utf-8")).decode(
                "ascii"
            )
        }

        service = build("gmail", "v1", credentials=self.creds)
        service.users().messages().send(
            userId="me", body=mail
        ).execute()  # pylint: disable=no-member
