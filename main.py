import dotenv
import os
from check_multiple_mail import check_multiple_mail

#account credentials
found = dotenv.find_dotenv('config.env')
dotenv.load_dotenv(found)
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

check_multiple_mail(USERNAME, PASSWORD, 6)