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

    @staticmethod
    def subject_from_message(message) -> str:
        headers = message["payload"]["headers"]

        return [h["value"] for h in headers if h["name"] == "Subject"][0]

    @staticmethod
    def timestamp_from_message(message) -> int:
        return int(message["internalDate"])

    def __init__(self, token_file, src_address, dst_address):
        self.creds = Mailer.__get_creds(token_file)
        self.src_address = src_address
        self.dst_address = dst_address

        self.service = build("gmail", "v1", credentials=self.creds)

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

        self.service.users().messages().send(  # pylint: disable=no-member
            userId="me", body=mail
        ).execute()

    def list_matching_query(self, query, max_results=10):
        response = (
            self.service.users()  # pylint: disable=no-member
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )

        if "messages" in response:
            return response["messages"]

        return []

    def get_message(self, message_id):
        message = (
            self.service.users()  # pylint: disable=no-member
            .messages()
            .get(userId="me", id=message_id)
            .execute()
        )

        return message
