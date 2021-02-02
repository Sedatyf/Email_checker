import imapclient, pyzmail
import os, sys

pwd = os.path.dirname(__file__)
attach_folder = os.path.join(pwd, "attachments")

def search_mail(username, password, imap, subject):
	imapObj = imapclient.IMAPClient(imap, ssl=True)
	imapObj.login(username, password)
	print(f"[+] You are connected as {username}")

	imapObj.select_folder('INBOX', readonly=True)
    
	print(f"[*] Looking for mail with the subject: {subject}")
	UID = imapObj.search(['SUBJECT', subject])
	if UID:
		print("[+] Mail found")
	else:
		print(f"[-] No mail found with the subject: {subject}\nExiting...")
		sys.exit()

	rawMessages = imapObj.fetch([UID[0]], ['BODY[]', 'FLAGS'])
	message = pyzmail.PyzMessage.factory(rawMessages[UID[0]][b'BODY[]'])

	for mailpart in message.mailparts:
		name = mailpart.filename
		if name is None:
			continue

		print(f"[+] Downloading attachment: {name}")
		payload = mailpart.get_payload()
		path = os.path.join(attach_folder, name)
		os.mkdir(attach_folder)
		open(path, 'wb').write(payload)
	
	if not os.path.exists(attach_folder):
		print(f"[-] No attachment found for mail with subject \"{subject}\"\nExiting...")
		sys.exit()

	if len(os.listdir(attach_folder)) > 0:
		return [os.path.join(attach_folder, f) for f in os.listdir(attach_folder) if os.path.isfile(os.path.join(attach_folder, f))]