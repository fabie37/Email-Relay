import requests
from gmailrelay import Relay
from env import API_KEY, EMAIL_LIST_ROUTE, SENDER
# API Access Keys
gmail_secret_filename = "gmail_client_secret.json"
aws_credentials = "aws_credentials.csv"
aws_config = "aws_config.json"

# FROM Attribute in email
sender = SENDER

# List of email addresses
req = requests.get(EMAIL_LIST_ROUTE, json={"API_KEY":API_KEY}, timeout=30)
json = req.json()
if (not json["success"] or json["success"] is False):
    print("Unable to get client list")
    exit()
client_list = [client["email"] for client in json["payload"]]

relay = Relay(gmail_secret_filename, aws_config, aws_credentials)
email = relay.get_first_unread_email(sender)
if email:
    relay.match_and_replace(email, r"(https?://(www.)?)?fabsapi\.com/((?!\")\S)+", "https://google.com")
    relay.send_mail(sender, client_list, email)
