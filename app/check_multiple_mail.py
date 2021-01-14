import imaplib
import email
import os, dotenv
import get_config

def check_multiple_mail(username, password, imap, number):
	attachments = 0
	mail = imaplib.IMAP4_SSL(imap)
	mail.login(username, password)

	_, messages = mail.select("INBOX")
	total_mail = int(messages[0])
	N = number

	for i in range(total_mail, total_mail - N, -1):
		_, msg = mail.fetch(str(i), "(RFC822)")

		for response in msg:
			if isinstance(response, tuple):
				msg = email.message_from_bytes(response[1])

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
								attachments += 1

	print(f"[+] Downloaded {attachments} attachments from your mailbox")

	mail.close()
	mail.logout()

	if attachments > 0:
		return [os.path.join(attach_folder, f) for f in os.listdir(attach_folder) if os.path.isfile(os.path.join(attach_folder, f))]

if __name__ == "__main__":
	#account credentials
	USERNAME = get_config.get_username()
	PASSWORD = get_config.get_password()
	IMAP = get_config.get_imap()

	check_multiple_mail(USERNAME, PASSWORD, IMAP, 6)