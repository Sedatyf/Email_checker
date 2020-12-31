import dotenv, os, argparse
from check_multiple_mail import check_multiple_mail
from search_mail import search_mail

#account credentials
found = dotenv.find_dotenv('config.env')
dotenv.load_dotenv(found)
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
IMAP = os.getenv('IMAP')

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", type=str, help="Search for a specific mail")
parser.add_argument("-m", "--multiple", type=int, help="Allow you to check multiple attachments")
args = parser.parse_args()

if args.search:
	order = input("Is this an old mail or a recent mail ? (O)ld / (R)ecent / (D)on't know? ")
	if order.lower() in ["o","d"]:
		search_mail(USERNAME, PASSWORD, IMAP, args.search)
	elif order.lower() == "r":
		search_mail(USERNAME, PASSWORD, IMAP, args.search, -1)
	else:
		print("Your answer must be O / R / D")
elif args.multiple:
	check_multiple_mail(USERNAME, PASSWORD, IMAP, args.multiple)