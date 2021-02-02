# Email Checker

## Requirements

You'll need an api key from VirusTotal in order to scan your file. You have to create an account in VirusTotal and then specify your key in the ``dotenv`` file as precised below.

You'll need to make a ``config.env`` file in the root folder in order to give private information about your account.
In this file you have to create three variables where those variables goes like this :

```env
USERNAME=<your_email_address>
PASSWORD=<your_email_password>
IMAP=<your_imap>
APIKEY=<your_virustotal_apikey>
```

In the ``IMAP`` you have to give the right imap service along your mailbox (Gmail, Outlook, Yahoo, etc.). You can find a list of IMAP here : <https://www.systoolsgroup.com/imap/>

## TODO

- Change check multiple to check unseen
- Try some CI/CD pipeline
- Check if I can automate process
  - From Thunderbird (?) : Make a thunderbird init
  - From Outlook/Gmail API (?)
  - Other solutions ?
- ~~Refactoring (guard clause, etc.)~~
- ~Make some test to see if it's working perfectly (I'm sure it misses some email)~
- GUI?
