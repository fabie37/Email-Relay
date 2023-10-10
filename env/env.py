import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
EMAIL_LIST_ROUTE = os.getenv('EMAIL_LIST_ROUTE')
SENDER = os.getenv('SENDER')
UNSUBSCRIBE_URL = os.getenv('UNSUBSCRIBE_URL')
HOST_URL = os.getenv('HOST_URL')
SEARCH_FOR = os.getenv('SEARCH_FOR')
