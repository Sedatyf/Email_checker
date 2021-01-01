import dotenv, os, argparse
from check_multiple_mail import check_multiple_mail
from search_mail import search_mail
import virustotal_requests as vt_r

#account credentials
found = dotenv.find_dotenv('config.env')
dotenv.load_dotenv(found)
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
IMAP = os.getenv('IMAP')

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-s", "--search", type=str, help="Search for a specific mail")
parser.add_argument("-a", "--age", type=str, choices=['o', 'r'], help="In the search context, precise if its an old mail or a recent mail")
parser.add_argument("-m", "--multiple", type=int, help="Allow you to check multiple attachments")
args = parser.parse_args()

if args.search:
	if args.age == "o":
		search_mail(USERNAME, PASSWORD, IMAP, args.search)
	elif args.age == "r":
		search_mail(USERNAME, PASSWORD, IMAP, args.search, -1)
	else:
		print(f"""[!!] In the search context, you have to precise if it's an old mail or a recent mail
Example: python3 {os.path.basename(__file__)} -s \"Hello World\" -a r""")

	vt_r.analyse_file()
	get_analysis("NWI5NGJmZTc4ZWFiOTFiYTE3OTczNTIyOGFiM2Y0OTg6MTYwOTUzMTU2NQ==")
elif args.multiple:
	check_multiple_mail(USERNAME, PASSWORD, IMAP, args.multiple)