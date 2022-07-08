from distutils.log import error
from logging import raiseExceptions
from operator import truediv
from time import sleep
from urllib import response
from certifi import contents
import requests
import json
from pprint import pprint
import os
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)






device = {"ip": os.getenv('switch_ip'), "port": "443", "user": os.getenv('switch_user'), "password": os.getenv('switch_pwd')}
interfaceName="1/0/20".replace("/","%2f")
baseUrl=f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet={interfaceName}/switchport/"
url = baseUrl+"Cisco-IOS-XE-switch:port-security-cfg"
headers = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
response = requests.delete(url=url,auth=(device['user'], device['password']),verify=False, headers=headers)





if response.status_code != 204:
    print("Failed")
    print(response.status_code)
    print(response.content)
else:
    print("WORKED!")


url = baseUrl+"Cisco-IOS-XE-switch:port-security-conf"
response = requests.delete(url=url,auth=(device['user'], device['password']),verify=False, headers=headers)
if response.status_code == 204:
    print("WORKED!")
elif response.status_code== 409:
    contents=response.content
    print("Failed")
    print(response.status_code)
    print(contents)
    obj=json.loads(contents)
    print(json.dumps(obj,indent=4))
    if "database is locked" in obj['errors']['error'][0]['error-message']:
        print("waiting 30 sec")
        sleep(30)
        response = requests.delete(url=url,auth=(device['user'], device['password']),verify=False, headers=headers)
