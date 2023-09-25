import csv
import json
import ssl
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SES():
    """
        This object iteracts with SES via the SMTP client baked into python.
        This results in easier to read code with being a lot more simple to write.
        Here we can send emails just like we were using any other email client.

        We is required is two files in your project directory.
        \n - smtp_credentials.csv - you can download this from your amazon console (under SMTP credentials)
        \n - aws_config.json - config file to change your host and port number
                    {
                     "host":"aws.com",
                     "port":"587"
                    }
        
        If you're worried about bulk sending, amazon even recommends simply iterating over your
        receiptents list and emailing them individualy. I suppose bulk email can only be optimised
        over template based emails. 

    """
    def __init__(self, credentials="aws_credentials.csv", config="aws_config.json"):
        self._read_credentials_csv(credentials)
        self._read_config(config)
    
    def sendmail(self, email):
        """
            Sends an email to given SMTP client.

            Args: 
                - email: This is a basic dictionary containing the details of the email.
                 {
                    "from": "me@sender.com",
                    "to": "receipent@gmail.com",
                    "subject": "Email Subject",
                    "plain": "Plain text of email",
                    "html": "<body> Html </body>"
                 }
        """
        context = ssl.create_default_context()
        with SMTP(self.host, self.port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self.smtp_user, self.smtp_password)
            msg = self._create_email(email)
            server.sendmail(email["from"], email["to"], msg.as_string())
  
    def _read_config(self, config):
        with open(config, encoding="ascii") as file:
            data = json.load(file)
            self.host = data["host"]
            self.port = data["port"]

    def _create_email(self, email):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = email["subject"]
        msg['From'] = email["from"]
        msg['To'] = email["to"]
        plain_part = MIMEText(email["plain"], 'plain')
        html_part = MIMEText(email["html"], 'html')
        msg.attach(plain_part)
        msg.attach(html_part)
        return msg
        
    def _read_credentials_csv(self, credentials):
        self.iam_user = None    
        self.smtp_user = None
        self.smtp_password = None
        try:
            with open(credentials, newline='', encoding='utf-8-sig') as csvfile:
                cred_reader = csv.DictReader(csvfile, delimiter=',')
                for row in cred_reader:
                    self.iam_user = row["IAM user name"]
                    self.smtp_user = row["SMTP user name"]
                    self.smtp_password = row["SMTP password"]
        except FileNotFoundError:
            print("Please add SES credential file to root directory.")
