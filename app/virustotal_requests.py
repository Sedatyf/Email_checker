import requests, json
import os, dotenv
import time

found = dotenv.find_dotenv('config.env')
dotenv.load_dotenv(found)
APIKEY = os.getenv("APIKEY")

headers = {'x-apikey': APIKEY}

def analyse_file(filepath):
    print("[+] Sending your file")

    file_to_send = {'file': open(filepath, 'rb')}

    send_file = requests.post(f"https://www.virustotal.com/api/v3/files", headers=headers, files=file_to_send)
    
    send_file.raise_for_status()
    resp_dict = send_file.json()
    id_file = json.dumps(resp_dict['data']['id']).replace('"', '')
    
    return id_file


def get_analysis(file_id):
    print("[+] Getting your results")

    get_analysis = requests.get(f"https://www.virustotal.com/api/v3/analyses/{file_id}", headers=headers)

    if get_analysis.status_code == requests.codes.ok:
        resp_dict = get_analysis.json()
        status = resp_dict['data']['attributes']['status']

        while status != "completed":
            get_analysis = requests.get(f"https://www.virustotal.com/api/v3/analyses/{file_id}", headers=headers)
            resp_dict = get_analysis.json()
            status = resp_dict['data']['attributes']['status']
            time.sleep(20)
        
        stats = json.dumps(resp_dict['data']['attributes']['stats'], indent=4).replace('"', '').replace('}', '').replace('{', '').replace(',', '')
        print(f"[+] Results of your scan: {stats}")

if __name__ == "__main__":
    id_file = analyse_file("/home/app/Email_checker/app/attachments/CMI1RIBS_FR_RibsImprRib.xml.pdf")
    get_analysis(id_file)