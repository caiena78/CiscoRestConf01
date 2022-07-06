from numpy import put
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
url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet"



payload=[]

payload.append({
    "Cisco-IOS-XE-native:GigabitEthernet": {
        "name": "1/0/20",
        "description" : "test",
        "Cisco-IOS-XE-spanning-tree:spanning-tree": {
            "bpduguard": {
                "enable": [
                    None
                ]
            },
            "portfast": {}
        },
        "switchport": {
            "Cisco-IOS-XE-switch:access": {
                "vlan": {
                    "vlan": 1164
                }
            },
            "Cisco-IOS-XE-switch:mode": {
                "access": {}
            },
            "Cisco-IOS-XE-switch:voice": {
                "vlan": {
                    "vlan": 1165
                }
            }
        }
    }
})

payload.append({
    "Cisco-IOS-XE-native:GigabitEthernet": {
        "name": "1/0/20",
         "switchport": {
            "Cisco-IOS-XE-switch:port-security-conf": {
                "port-security": {
                    "mac-address": {
                        "sticky": [
                            None
                        ]
                    },
                    "maxcount": [
                        {
                            "max-addresses": 1,
                            "vlan": "voice"
                        },
                        {
                            "max-addresses": 2
                        }
                    ],
                    "violation": {
                        "restrict": [
                            None
                        ]
                        }
                }
            }
             
        }
        
    }
})

payload.append({
    "Cisco-IOS-XE-native:GigabitEthernet": {
        "name": "1/0/20",
         "switchport": {
            "Cisco-IOS-XE-switch:port-security-conf": {
                "port-security": {
                    "maxcount": [
                        {
                            "max-addresses": 1,
                            "vlan": "access"
                        }
                    ]
                }
            }
             
        }
        
    }
})

cnt=1
for item in payload:
    str_payload=json.dumps(item)
    if cnt==0:
       data=putdata(device,url,str_payload)
    else:
        data=patchdata(device,url,str_payload)
    cnt=cnt+1
    if data.status_code >200 and data.status_code < 300:
        print("Success")
    print(data.status_code)
    print(data.content)