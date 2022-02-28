import imaplib
import base64
import os
import email


class Email:
    def __init__(self, email, password):
        self.email_user = email
        self.email_pass = password
        self.host = "imap.gmail.com"
        self.port = 993

    def login(self):
        mail = imaplib.IMAP4_SSL(self.host, self.port)
        mail.login(self.email_user, self.email_pass)
        mail.select("Inbox")
        result, data = mail.search(
            None, '(FROM "kartikeya sharma" SUBJECT "test")')
        ids = data[0]  # data is a list.
        id_list = ids.split()  # ids is a space separated string
        latest_email_id = id_list[-1]  # get the latest
        # fetch the email body (RFC822)             for the given ID
        result, data = mail.fetch(latest_email_id, "(RFC822)")
        # here's the body, which is raw text of the whole email
        raw_email = data[0][1]
        # including headers and alternate payloads
