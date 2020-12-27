import imaplib
import email
from email.header import decode_header
import dotenv
import os

def search_mail(username, password, mail_object, order=1):
	found = False
	mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")
	mail.login(username, password)

	status, messages = mail.select("INBOX")
	total_mail = int(messages[0])
	start = 1
	end = total_mail + 1
	
	if order == -1:
		start = total_mail
		end = 0
	
	for i in range(start, end, order):
		_, msg = mail.fetch(str(i), "(RFC822)")
		
		for response in msg:
			if isinstance(response, tuple):
				msg = email.message_from_bytes(response[1])
				
				subject, encoding = decode_header(msg["Subject"])[0]
				if isinstance(subject, bytes):
					try:
						subject = subject.decode(encoding)
					except TypeError:
						pass
				
				if subject == mail_object:
					print("Mail found")
					content_type = msg.get_content_type()
			
					if msg.is_multipart():
						for part in msg.walk():
							content_disposition = str(part.get("Content-Disposition"))
							if "attachment" in content_disposition:
								filename = part.get_filename()
								if filename:
									pwd = os.path.dirname(__file__)
									attach_folder = os.path.join(pwd, "attachments")
								
									try:
										os.mkdir(attach_folder)
									except FileExistsError:
										pass
								
									filepath = os.path.join(attach_folder, filename)
									open(filepath, "wb").write(part.get_payload(decode=True))
					found = True
				else:
					print("Mail does not match given subject")
		if found:
			break
	mail.close()
	mail.logout()

if __name__ == "__main__":
	#account credentials
	found = dotenv.find_dotenv('config.env')
	dotenv.load_dotenv(found)
	USERNAME = os.getenv('USERNAME')
	PASSWORD = os.getenv('PASSWORD')
	
	search_mail(USERNAME, PASSWORD, "RIB")