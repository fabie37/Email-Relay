# Gmail to Amazon SES Relay

**What is this?**

This is a simple application to grab an email from you gmail inbox, edit it, then send it to a email distribution service of your chosing.

**How does it work?**

Couldn't be easier! All that is needed is an gmail application access key and an amazon ses key. Once you have them, you can read from your gmail inbox, edit an email and send it off to a client list.

***Required Permissions***

- Google Client OAuth 2.0 Secret: https://console.cloud.google.com/apis 
    - Login to google cloud api
    - Create a new project
    - Enable gmail api
    - Choose a client based Oath Credential 
    - Download client_secret.json
    - Store in root directory
- Amazon SES Client Auth


## Example of gmail_client_secret.json

This should be automatically created by the google api console. Just download it.
This is an example of a desktop application.

```
{"installed":
    {"client_id":"YOUR CLIENT ID",
    "project_id":"YOUR_PROJECT_ID",
    "auth_uri":"https://accounts.google.com/o/oauth2/auth",
    "token_uri":"https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
    "client_secret":"YOUR_SECRET",
    "redirect_uris":["http://localhost"]}
}
```

## Example of amazon_client_secret.json

Just manually create this in your root directory. 

```
{
    "aws_access_key_id": "YOUR ACCESS KEY ID",
    "aws_secret_access_key": "YOUR SECRET KEY"
}
```



# Usage

### Reading an email and batch sending it:
```
from gmailrelay import Relay

# API Access Keys & Config Files
gmail_secret_filename = "gmail_client_secret.json"
aws_credentials = "aws_credentials.csv"
aws_config = "aws_config.json"

# The from address your clients will see
sender = "you@example.com"

client_list = ["a@mail.com", "b@mail.com"...]

relay = Relay(gmail_secret_filename, aws_config, aws_credentials)

email = relay.get_first_unread_email("sender@mail.com")
relay.match_and_replace(email, "REGULAR_EXPRESSION", "TEXT_TO_INSERT")

relay.send(sender, client_list, email)
```