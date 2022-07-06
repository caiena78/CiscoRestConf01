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

# put replaces the existing config on the interface.
def putdata(device,url,payload):
    headers = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
    response = requests.put(url=url,data=payload,auth=(device['user'], device['password']),verify=False, headers=headers)
    return  response

#leaves existing config in place and adds the data in the payload to the interface
def patchdata(device,url,payload):
    headers = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
    response = requests.patch(url=url,data=payload,auth=(device['user'], device['password']),verify=False, headers=headers)
    return  response

# set up connection parameters in a dictionary
device = {"ip": os.getenv('switch_ip'), "port": "443", "user": os.getenv('switch_user'), "password": os.getenv('switch_pwd')}



id=encodeInterface("1/0/20")
url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet={id}"

payload= """
  {
    "Cisco-IOS-XE-native:GigabitEthernet": {
        "name": "1/0/20",
        "shutdown": [
            null
        ]
    }
}
"""

url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet"

payload= """
  {
    "Cisco-IOS-XE-native:GigabitEthernet": {
        "name": "1/0/20",
        "description": "test"
    }
}
"""




data=patchdata(device,url,payload)
print(data)

