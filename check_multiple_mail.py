import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os

def check_multiple_mail(username, password, number):
	mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")
	mail.login(username, password)

	status, messages = mail.select("INBOX")
	total_mail = int(messages[0])
	N = number

	for i in range(total_mail, total_mail - N, -1):
		_, msg = mail.fetch(str(i), "(RFC822)")
	
		for response in msg:
			if isinstance(response, tuple):
				msg = email.message_from_bytes(response[1])
				content_type = msg.get_content_type()
			
				if msg.is_multipart():
					for part in msg.walk():
						content_disposition = str(part.get("Content-Disposition"))
						if "attachment" in content_disposition:
							filename = part.get_filename()
							if filename:
								pwd = os.path.dirname(__file__)
								filepath = os.path.join(pwd, filename)
								open(filepath, "wb").write(part.get_payload(decode=True))

	mail.close()
	mail.logout()

if __name__ == "__main__":
	#account credentials
	found = dotenv.find_dotenv('config.env')
	dotenv.load_dotenv(found)
	USERNAME = os.getenv('USERNAME')
	PASSWORD = os.getenv('PASSWORD')

	check_multiple_mail(USERNAME, PASSWORD, 6)