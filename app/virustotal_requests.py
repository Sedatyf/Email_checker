import requests, json
import os, dotenv
import time

found = dotenv.find_dotenv('config.env')
dotenv.load_dotenv(found)
APIKEY = os.getenv("APIKEY")

headers = {'x-apikey': APIKEY}

def analyse_file(file_list):
    print("[+] Sending your file to Virus Total")
    if len(file_list) > 4:
        print("[!!] You have to many files to send. API limit is 4")
    else:
        id_list = []

        for attach in file_list:
            file_to_send = {'file': open(attach, 'rb')}

            send_file = requests.post(f"https://www.virustotal.com/api/v3/files", headers=headers, files=file_to_send)

            send_file.raise_for_status()

            resp_dict = send_file.json()
            id_file = json.dumps(resp_dict['data']['id']).replace('"', '')
            id_list.append(id_file)

            print(f"[+] Your file {os.path.basename(attach)} has the following id: {id_file}")

        return id_list


def get_analysis(id_list):
    print("[+] Getting your results")

    for file_id in id_list:
        get_analysis = requests.get(f"https://www.virustotal.com/api/v3/analyses/{file_id}", headers=headers)

        if get_analysis.status_code == requests.codes.ok:
            print("[+] Succeeded request, waiting analysis to be completed")
            resp_dict = get_analysis.json()
            status = resp_dict['data']['attributes']['status']

            while status != "completed":
                get_analysis = requests.get(f"https://www.virustotal.com/api/v3/analyses/{file_id}", headers=headers)
                resp_dict = get_analysis.json()
                status = resp_dict['data']['attributes']['status']
                time.sleep(20)
        
            stats = json.dumps(resp_dict['data']['attributes']['stats'], indent=4).replace('"', '').replace('}', '').replace('{', '').replace(',', '')
            current_file = os.path.basename(file_id)
            print(f"[+] Results of your scan for {current_file}: {stats}")

if __name__ == "__main__":
    some_file = ['/home/app/Email_checker/app/attachments/Chelou.pdf']
    id_file = analyse_file(some_file)

    some_id = ["ZGUxNjJmYzI4ZDRkOGVmY2M4YmViNWNiOWQ4ZjczY2M6MTYwOTU0MDU0OA=="]
    get_analysis(some_id)