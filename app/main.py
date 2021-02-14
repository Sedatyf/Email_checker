import os, argparse, sys
from check_unseen import check_unseen
from search_mail import search_mail
import virustotal_requests as vt_r
import get_config

#account credentials
USERNAME = get_config.get_username()
PASSWORD = get_config.get_password()
IMAP = get_config.get_imap()

parser = argparse.ArgumentParser(description="Create a sandbox to check if your mail's attachments are safe")
parser.add_argument("-s", "--search", nargs='+', help="Search for a specific mail")
parser.add_argument("-m", "--multiple", help="Allow you to check multiple attachments", action="store_true")
parser.add_argument("-r", "--report", help="Print a report in a text file", action="store_true")
args = parser.parse_args()

if args.search:
	list_file = search_mail(USERNAME, PASSWORD, IMAP, ' '.join(args.search))
	if list_file is None:
		print("[!!] No file detected. Stopping...")
		sys.exit()

	vt_r.handle_attachments(list_file)

elif args.multiple:
	list_file = check_unseen(USERNAME, PASSWORD, IMAP)

	if list_file is None:
		print("[!!] No file detected. Stopping...")
		sys.exit()
		
	if args.report:
		vt_r.handle_attachments(list_file, 'y')
	else:
		vt_r.handle_attachments(list_file)