from gmailrelay import Relay
# API Access Keys
gmail_secret_filename = "gmail_client_secret.json"
aws_credentials = "aws_credentials.csv"
aws_config = "aws_config.json"

sender = "fabrizio@catinella.co.uk"

client_list = [sender]

relay = Relay(gmail_secret_filename, aws_config, aws_credentials)
email = relay.get_first_unread_email(sender)
relay.match_and_replace(email, r"(https?://(www.)?)?fabsapi\.com/((?!\")\S)+", "https://google.com")
relay.send_mail(sender, client_list, email)
