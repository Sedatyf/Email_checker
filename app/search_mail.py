import imaplib
import email
from email.header import decode_header
import dotenv, os
import get_config

def search_mail(username, password, imap, mail_object, order=1):
	found = False
	mail = imaplib.IMAP4_SSL(imap)
	mail.login(username, password)

	_, messages = mail.select("INBOX")
	total_mail = int(messages[0])
	start = 1
	end = total_mail + 1
	
	if order == -1:
		start = total_mail
		end = 0
	
	print("[+] Searching your mail")
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
					print("[+] Mail found")
			
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

		if found:
			break

	mail.close()
	mail.logout()

	files = [os.path.abspath(os.path.join(attach_folder, f)) for f in os.listdir(attach_folder) if os.path.isfile(os.path.join(attach_folder, f))]
	return files

if __name__ == "__main__":
	#account credentials
	USERNAME = get_config.get_username()
	PASSWORD = get_config.get_password()
	IMAP = get_config.get_imap()
	
	search_mail(USERNAME, PASSWORD, IMAP, "RIB", -1)