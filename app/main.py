import os, argparse, sys
from check_multiple_mail import check_unseen
from search_mail import search_mail
import virustotal_requests as vt_r
import get_config

#account credentials
USERNAME = get_config.get_username()
PASSWORD = get_config.get_password()
IMAP = get_config.get_imap()

parser = argparse.ArgumentParser(description="Create a sandbox to check if your mail's attachments are safe")
parser.add_argument("-s", "--search", type=str, nargs='+', help="Search for a specific mail")
parser.add_argument("-a", "--age", type=str, choices=['o', 'r'], help="In the search context, precise if its an old mail or a recent mail")
parser.add_argument("-m", "--multiple", help="Allow you to check multiple attachments", action="store_true")
args = parser.parse_args()

if args.search:
	if args.age == "o":
		list_file = search_mail(USERNAME, PASSWORD, IMAP, ' '.join(args.search))
		if not list_file is None:
			id_list = vt_r.analyse_file(list_file)
			vt_r.get_analysis(id_list)
		else:
			print("[!!] No file detected. Stopping...")
			sys.exit()

	elif args.age == "r":
		list_file = search_mail(USERNAME, PASSWORD, IMAP, ' '.join(args.search))
		if not list_file is None:
			id_list = vt_r.analyse_file(list_file)
			vt_r.get_analysis(id_list)
		else:
			print("[!!] No file detected. Stopping...")
			sys.exit()

	else:
		print(f"""[!!] In the search context, you have to precise if it's an old mail or a recent mail
Example: python3 {os.path.basename(__file__)} -s \"Hello World\" -a r""")

elif args.multiple:
	list_file = check_unseen(USERNAME, PASSWORD, IMAP)

	if not list_file is None:
		id_list = vt_r.analyse_file(list_file)
		vt_r.get_analysis(id_list)
	else:
		print("[!!] No file detected. Stopping...")
		sys.exit()