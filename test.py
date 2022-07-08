from logging import raiseExceptions
from operator import truediv
import string
from urllib import response
import requests
import json
from pprint import pprint
import os
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import datetime
from enum import Flag



class vlantype(Flag):
    access=1
    voice=2

class policyDirection(Flag):
    direction_in=1
    direction_out=2

def errorCheck(response:response):
    if response.status_code >399:
        print(response.status_code)
        print(response.content)
        return True
    return False 


def encodeInterface(strInterface):
    strInterface = strInterface.replace("/","%2f")
    return strInterface

def getdata(device,url):
    headers = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
    response = requests.get(url, headers=headers, auth=(device['user'], device['password']), verify=False)
    if errorCheck(response):
        quit()
    return response.json()

# put replaces the existing config on the interface.
def putdata(device,url,payload):
    headers = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
    response = requests.put(url=url,data=payload,auth=(device['user'], device['password']),verify=False, headers=headers)
    if errorCheck(response):
        quit()
    return response.json()

#leaves existing config in place and adds the data in the payload to the interface
def patchdata(device,url,payload):
    headers = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}
    response = requests.patch(url=url,data=payload,auth=(device['user'], device['password']),verify=False, headers=headers)
    if errorCheck(response):
        quit()
    try:
        returndata=response.json()
    except:
        returndata=response
    return returndata


def getInterface(device,interfaceName:string):
    interfaceName=encodeInterface(interfaceName)
    url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet={interfaceName}"
    return getdata(device,url)

def chkAccess(interface):
    if "switchport" not in interface["Cisco-IOS-XE-native:GigabitEthernet"]:
        return False
    return True

def raiseError(error:string):
    raise Exception(error)

def chkAccessMode(interface):
    if chkAccess(interface) == False:
        return False
    if  "Cisco-IOS-XE-switch:mode" not in interface["Cisco-IOS-XE-native:GigabitEthernet"]["switchport"]:
        return False
    if "access" not in interface["Cisco-IOS-XE-native:GigabitEthernet"]["switchport"]["Cisco-IOS-XE-switch:mode"]:    
        return False
    return True

def setAccessMode(device,interface):
    print("Set Access Mode")
    accessMode={ 
        "switchport": {
            "Cisco-IOS-XE-switch:mode": {
                "access": {}
            }
        }
    }
    interface["Cisco-IOS-XE-native:GigabitEthernet"]['switchport']=accessMode['switchport']
    url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet"
    patchdata(device,url,json.dumps(interface))
    return interface

def chkVoiceVlan(interface):
    if chkAccess(interface)==False:
        return False
    if "Cisco-IOS-XE-switch:voice" not in interface["Cisco-IOS-XE-native:GigabitEthernet"]['switchport']:
        return False
    if "vlan" not in interface["Cisco-IOS-XE-native:GigabitEthernet"]['switchport']["Cisco-IOS-XE-switch:voice"]:
        return False
    return True



def setVlan(device,interface,vlantype:vlantype,vlan):
    if vlantype==vlantype.access:
        print("Set Access Vlan")
        interface["Cisco-IOS-XE-native:GigabitEthernet"]['switchport']["Cisco-IOS-XE-switch:access"]= {"vlan": { "vlan" : vlan}}
    if vlantype==vlantype.voice:
        print("Set Voice Vlan")
        interface["Cisco-IOS-XE-native:GigabitEthernet"]['switchport']["Cisco-IOS-XE-switch:voice"]= {"vlan": { "vlan" : vlan}}
    url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet"
    patchdata(device,url,json.dumps(interface))


def enablePortSecurity(device,interface):
    if chkAccessMode(interface) == False:
        interface=setAccessMode(device,interface)
    if chkVoiceVlan(interface) == False:
        setVlan(device,interface,vlantype.access,1164)
        setVlan(device,interface,vlantype.voice,1165)
    interface["Cisco-IOS-XE-native:GigabitEthernet"]['switchport']["Cisco-IOS-XE-switch:port-security-conf"]={
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
    url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet"
    print("Enable PortSecurity")
    patchdata(device,url,json.dumps(interface))
    return interface

def servicePolicy(device,interface,direction:policyDirection,policyName:string):
    if direction == policyDirection.direction_in:
        print("Service Policy in")
        interface["Cisco-IOS-XE-native:GigabitEthernet"]["Cisco-IOS-XE-policy:service-policy"]={
            "input": policyName,
            }
    if direction==policyDirection.direction_out:
            print("Service Policy out")
            interface["Cisco-IOS-XE-native:GigabitEthernet"]["Cisco-IOS-XE-policy:service-policy"]={
                "output": policyName
            }      
    url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet"
    patchdata(device,url,json.dumps(interface))
    return interface

def bpduGurad(device,interface):
    print("BPDU Guard and Portfast")
    url = f"https://{device['ip']}:{device['port']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet"
    interface["Cisco-IOS-XE-native:GigabitEthernet"]["Cisco-IOS-XE-spanning-tree:spanning-tree"]={
            "bpduguard": {
                "enable": [None]
            },
            "portfast": {}
    }
    patchdata(device,url,json.dumps(interface))
    return interface  


# set up connection parameters in a dictionary
device = {"ip": os.getenv('switch_ip'), "port": "443", "user": os.getenv('switch_user'), "password": os.getenv('switch_pwd')}


interface=getInterface(device,"1/0/20")
interface=enablePortSecurity(device,interface)
interface=servicePolicy(device,interface,policyDirection.direction_in,"INPUT-CISCOPHONE-POLICY")
interface=servicePolicy(device,interface,policyDirection.direction_out,"OUTPUT-PHONE")
interface=bpduGurad(device,interface)

print(json.dumps(interface,indent=4))