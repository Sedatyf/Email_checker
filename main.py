import dotenv
import os
from check_multiple_mail import check_multiple_mail
import argparse

#account credentials
found = dotenv.find_dotenv('config.env')
dotenv.load_dotenv(found)
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--multiple", type=int, help="Allow you to check multiple attachments")
args = parser.parse_args()

if args.multiple:
	check_multiple_mail(USERNAME, PASSWORD, args.multiple)