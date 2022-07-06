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


def disableCheck(interface,disabledate):
    discontinuitytime=datetime.datetime.fromisoformat(interface['statistics']['discontinuity-time'])
    print("discontinuitytime: %s" % discontinuitytime)
    if "*!*" in interface['description']:
        print("Skipping interface")
        return False
    if interface['admin-status'] != 'if-state-up':
        print("Interface is Disabled")
        return False
    if interface['oper-status'] == 'if-oper-state-ready':
      # if-oper-state-ready - this means connectied
        print("interface is connected")
        return False
    if discontinuitytime.date() < disabledate.date():
        return True
    else:
        return False

# set up connection parameters in a dictionary
device = {"ip": os.getenv('switch_ip'), "port": "443", "user": os.getenv('switch_user'), "password": os.getenv('switch_pwd')}

#device = {"ip": "192.168.164.5", "port": "443", "user": "ca14028", "password": "Ilovemywifeandkids07"}


url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface"

api_data = getdata(device,url)

data=json.dumps(api_data,indent=4,sort_keys=True)
print(data)
with open("all_interfaces-cfg.json",'w') as w:
    w.write(data)