import dotenv, os

def get_username():
    found = dotenv.find_dotenv('config.env')
    dotenv.load_dotenv(found)
    return os.getenv('USERNAME')

def get_password():
    found = dotenv.find_dotenv('config.env')
    dotenv.load_dotenv(found)
    return os.getenv('PASSWORD')

def get_imap():
    found = dotenv.find_dotenv('config.env')
    dotenv.load_dotenv(found)
    return os.getenv('IMAP')

def get_apikey():
    found = dotenv.find_dotenv('config.env')
    dotenv.load_dotenv(found)
    return os.getenv("APIKEY")