import requests
import json
from pprint import pprint
import os
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import datetime



def getdata(device,url):
    headers = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
    response = requests.get(url, headers=headers, auth=(device['user'], device['password']), verify=False)
    return response.json()


device = {"ip": os.getenv('switch_ip'), "port": "443", "user": os.getenv('switch_user'), "password": os.getenv('switch_pwd')}   

url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces"

api_data = getdata(device,url)

data=json.dumps(api_data,indent=4,sort_keys=True)
print(data)
with open("all_interfaces.json",'w') as w:
    w.write(data)