import requests, json
import os, time
import get_config, getpass

APIKEY = get_config.get_apikey()

headers = {'x-apikey': APIKEY}

project_folder = os.path.dirname(__file__)
report_folder = os.path.join(project_folder, 'reports')

def handle_attachments(file_list, report='n'):
    if report.lower() == 'n':
        for attach in file_list:
            id_file = send_file(attach)
            get_analysis(id_file[1])

    elif report.lower() == 'y':
        os.mkdir(report_folder)
        for attach in file_list:
            id_file = send_file(attach)
            stats = get_analysis(id_file[1])

            report_file = id_file[0] + '_report.txt'
            report_path = os.path.join(report_folder, report_file) 
            with open(report_path, 'w') as f:
                f.write(f"[+] Results of your scan for {stats[1]}: {stats[0]}")
        print("Your reports have been printed in /tmp/reports/")

def send_file(attach):
    print(f"[*] Sending your file {attach} to VirusTotal")

    file_to_send = {'file': open(attach, 'rb')}

    send_file = requests.post(f"https://www.virustotal.com/api/v3/files", headers=headers, files=file_to_send)

    send_file.raise_for_status()

    resp_dict = send_file.json()
    id_file = json.dumps(resp_dict['data']['id']).replace('"', '')

    print(f"[+] Your file {os.path.basename(attach)} has the following id: {id_file}")

    return os.path.basename(attach), id_file


def get_analysis(id_file):
    print(f"[+] Getting results for the file with id {id_file}")

    get_analysis = requests.get(f"https://www.virustotal.com/api/v3/analyses/{id_file}", headers=headers)

    if get_analysis.status_code == requests.codes.ok:
        print("[+] Succeeded request, waiting analysis to be completed")
        resp_dict = get_analysis.json()
        status = resp_dict['data']['attributes']['status']

        while status != "completed":
            get_analysis = requests.get(f"https://www.virustotal.com/api/v3/analyses/{id_file}", headers=headers)
            resp_dict = get_analysis.json()
            status = resp_dict['data']['attributes']['status']
            time.sleep(10)
        
        stats = json.dumps(resp_dict['data']['attributes']['stats'], indent=4).replace('"', '').replace('}', '').replace('{', '').replace(',', '')
        current_file = os.path.basename(id_file)
        print_results(current_file, stats)
    
    return stats, current_file

def print_results(current_file, stats):
    print(f"[+] Results of your scan for {current_file}: {stats}")