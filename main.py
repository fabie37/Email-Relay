import requests
from gmailrelay import Relay
from env import API_KEY, EMAIL_LIST_ROUTE, SENDER, UNSUBSCRIBE_URL, HOST_URL, SEARCH_FOR
# API Access Keys
gmail_secret_filename = "gmail_client_secret.json"
aws_credentials = "aws_credentials.csv"
aws_config = "aws_config.json"

# FROM Attribute in email
sender = SENDER

# Email address to search emails form
search_for = SEARCH_FOR

# List of email addresses
req = requests.get(EMAIL_LIST_ROUTE, json={"API_KEY":API_KEY}, timeout=30)
json = req.json()
if (not json["success"] or json["success"] is False):
    print("Unable to get client list")
    exit()
client_list = [client for client in json["payload"]]

relay = Relay(gmail_secret_filename, aws_config, aws_credentials)
email = relay.get_first_unread_email(search_for)
if email:
    for client in client_list:
        relay.match_and_replace(email, r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&=]*)', HOST_URL)
        relay.match_and_replace(email, r'(?<=href=\")[^\"]*(?=".*>Unsubscribe<\/a>)', UNSUBSCRIBE_URL + '/' + client['hash'])
        relay.send_mail(sender, client["email"], email)

print("Finished Script.")
