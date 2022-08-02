import requests
import json
from pprint import pprint
import os
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import datetime


def encodeInterface(strInterface):
    strInterface = strInterface.replace("/","%2f")
    return strInterface

def getdata(device,url):
    headers = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
    response = requests.get(url, headers=headers, auth=(device['user'], device['password']), verify=False)
    return response.json()




# set up connection parameters in a dictionary
device = {"ip": os.getenv('switch_ip'), "port": "443", "user": os.getenv('switch_user'), "password": os.getenv('switch_pwd')}


id=encodeInterface("1/0/9")
url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet={id}"

api_data = getdata(device,url)

data=json.dumps(api_data,indent=4,sort_keys=True)
print(api_data['Cisco-IOS-XE-native:GigabitEthernet']['switchport']["Cisco-IOS-XE-switch:port-security-conf"]['port-security']["mac-address"]['sticky'])
with open("gi1-0-9-cfg.json",'w') as w:
    w.write(data)
