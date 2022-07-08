

#this does not work

def accumulate_keys(dct): # returns all the keys
    key_list = []
    def accumulate_keys_recursive(dct): # will accumulate keys in key_list
        for key in dct.keys():
            if isinstance(dct[key], dict):
                accumulate_keys_recursive(dct[key])
            else:
                key_list.append(key)
    accumulate_keys_recursive(dct)
    return key_list


dct={
    "Cisco-IOS-XE-native:GigabitEthernet": {
        "Cisco-IOS-XE-policy:service-policy": {
            "input": "INPUT-CISCOPHONE-POLICY",
            "output": "OUTPUT-PHONE"
        },
        "Cisco-IOS-XE-spanning-tree:spanning-tree": {
            "bpduguard": {
                "enable": [
                    None
                ]
            },
            "portfast": {}
        },
        "description": "TEST",
        "name": "1/0/9",
        "switchport": {
            "Cisco-IOS-XE-switch:access": {
                "vlan": {
                    "vlan": 1164
                }
            },
            "Cisco-IOS-XE-switch:mode": {
                "access": {}
            },
            "Cisco-IOS-XE-switch:port-security-cfg": [
                None
            ],
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
            },
            "Cisco-IOS-XE-switch:voice": {
                "vlan": {
                    "vlan": 1165
                }
            }
        }
    }
}
print(accumulate_keys(dct))

