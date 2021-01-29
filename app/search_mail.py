import imaplib
import email
from email.header import decode_header
import dotenv, os, sys
import get_config

def search_mail(username, password, imap, mail_object, order=1):
	attachments = 0
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
			if not isinstance(response, tuple):
				raise Exception("Your email is not following RFC822 rules") from ValueError
			
			msg = email.message_from_bytes(response[1])
			subject, encoding = decode_header(msg["Subject"])[0]
			if not isinstance(subject, bytes):
				return

			try:
				subject = subject.decode(encoding)
			except TypeError:
				pass
				
			if subject != mail_object:
				return
			print("[+] Mail found")
			
			if not msg.is_multipart():
				return
			for part in msg.walk():
				content_disposition = str(part.get("Content-Disposition"))
				if not "attachment" in content_disposition:
					return
				filename = part.get_filename()
				if not filename:
					return
				pwd = os.path.dirname(__file__)
				attach_folder = os.path.join(pwd, "attachments")			
			
				filepath = os.path.join(attach_folder, filename)
				open(filepath, "wb").write(part.get_payload(decode=True))
				attachments += 1
				found = True

		if found:
			break
		
	if not found:
		print(f"[-] No mail found with subject {mail_object}. Stopping...")
		sys.exit()

	mail.close()
	mail.logout()

	if attachments > 0:
		return [os.path.join(attach_folder, f) for f in os.listdir(attach_folder) if os.path.isfile(os.path.join(attach_folder, f))]

if __name__ == "__main__":
	#account credentials
	USERNAME = get_config.get_username()
	PASSWORD = get_config.get_password()
	IMAP = get_config.get_imap()
	
	search_mail(USERNAME, PASSWORD, IMAP, "RIB", -1)