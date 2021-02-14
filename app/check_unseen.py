import imapclient, pyzmail
import os, sys
import get_config

pwd = os.path.dirname(__file__)
attach_folder = os.path.join(pwd, "attachments")

def check_unseen(username, password, imap):
    imapObj = imapclient.IMAPClient(imap, ssl=True)
    imapObj.login(username, password)
    print(f"[+] You are connected as {username}")
    
    imapObj.select_folder('INBOX', readonly=True)
    
    print(f"[*] Looking for unseen mails")
    UIDs = imapObj.search("UNSEEN")
    if UIDs:
        print(f"[+] You have {len(UIDs)} unseen mails.")
    else:
        print(f"[-] No unseen mails found.\nExiting...")
        sys.exit()

    for i in range(0,len(UIDs)):
        rawMessages = imapObj.fetch([UIDs[i]], ['BODY[]', 'FLAGS'])
        message = pyzmail.PyzMessage.factory(rawMessages[UIDs[i]][b'BODY[]'])

        for mailpart in message.mailparts:
            name = mailpart.filename
            if name is None:
                continue
        
            print(f"[+] Downloading attachment: {name}")
            payload = mailpart.get_payload()
            path = os.path.join(attach_folder, name)
            
            if not os.path.exists(attach_folder):
                os.mkdir(attach_folder)
            open(path, 'wb').write(payload)
        
    if not os.path.exists(attach_folder):
        print(f"[-] No attachment found in your unseen mail.\nExiting...")
        sys.exit()
        
    if len(os.listdir(attach_folder)) > 0:
        return [os.path.join(attach_folder, f) for f in os.listdir(attach_folder) if os.path.isfile(os.path.join(attach_folder, f))]

if __name__ == "__main__":
    USERNAME = get_config.get_username()
    PASSWORD = get_config.get_password()
    IMAP = get_config.get_imap()
    check_unseen(USERNAME, PASSWORD, IMAP)