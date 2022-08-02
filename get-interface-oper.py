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



url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet1%2F0%2F2/"

api_data = getdata(device,url)




disabledate=datetime.datetime.today() - datetime.timedelta(days=30)

if disableCheck(api_data['Cisco-IOS-XE-interfaces-oper:interface'],disabledate):
    print("Disable Port")
    print(api_data['Cisco-IOS-XE-interfaces-oper:interface']['name'])
    print(api_data['Cisco-IOS-XE-interfaces-oper:interface']['description'])
    print(api_data['Cisco-IOS-XE-interfaces-oper:interface']['admin-status'])
    print(api_data['Cisco-IOS-XE-interfaces-oper:interface']['oper-status'])
    


