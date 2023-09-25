"""
    File: relay.py

    This module contains the implementation of the relay object.

"""
from typing import Optional
import re
from simplegmail import Gmail
from simplegmail.message import Message
from simplegmail.query import construct_query
from gmailrelay.ses import SES


class Relay:
    """
        The relay object is bridge between your gmail account and Amazon Ses.
        This class should be used as a top level object in your code. 
    """
    def __init__(self, gmail_secret_filename:str, aws_config_filename:str, aws_credentials_filename:str):
        self.gmail = Gmail(client_secret_file=gmail_secret_filename)
        self.gmail.maxResults = 10
        self.gmail_secret_filename = gmail_secret_filename
        self.aws_config_filename = aws_config_filename
        self.aws_credentials_filename = aws_credentials_filename
        self.ses = SES(aws_credentials_filename, aws_config_filename)
    
    def send_mail(self, sender:str, receipients:[str], email:Message):
        message = {}
        message['from'] = sender
        message['subject'] = email.subject
        message['plain'] = email.plain
        message['html'] = email.html

        for r in receipients:
            message['to'] = r
            try:
                self.ses.sendmail(message)
                print(f"Successfully sent email to {r}")
            except ConnectionError as connection_err:
                print(f"Failed to send mail to {r}")
                print(connection_err)
        
        print("Done sending")

    def get_first_unread_email(self, email_address:str, read:bool=True) -> Optional[Message]:
        """
            Gets the first available email, in the unread email box given an email address.
            Will automatically mark the message as read by default (read=True)

            Attributes:
                email_address : Str ~ The target email address to read from
                read:bool = True    ~ If true, marks email as read in your inbox.

            Return value:
                Optional : Message | None
        """
        query = {
            "sender":email_address,
            "unread":True}
        messages = self.gmail.get_messages(query=construct_query(query), attachments='reference')
        if messages:
            if read:
                messages[0].mark_as_read()
            return messages[0]
        return None
    
    @staticmethod
    def match_and_replace(email:Message, reg_exp:str, replace_with:str):
        """
            Matches a regular expression within a Message obj and replaces it with a string

            Attributes:
                email : Message
                reg_exp: Str
                replace_with: Str
            
        """
        if email:
            email.html = re.sub(reg_exp, replace_with, email.html) if email.html else None
            email.plain = re.sub(reg_exp, replace_with, email.plain) if email.plain else None





