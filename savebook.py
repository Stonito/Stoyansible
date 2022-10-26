"""
savebook.py

Saves the configuration of list of given hosts and returns state of the made changes

"""

import hosts
from IOS.ios import ios_save
from termcolor import colored

def save():
    hostStateChange= {}

    if platform == "ios":
        hostStateChange = ios_save(hostsToSave, hostStateChange)
    else:
        pass

    for host,state in hostStateChange.items():
        if state == "New configuration saved!":
            print(colored(f"{host} : {state}", 'green'))
        else:
            print(colored(f"{host} : {state}", 'yellow'))

### Admin-defined variables
##############################
platform = "ios"    ### Platform of configured devices - ios, huawei, mikrotik, etc.
hostsToSave = hosts.cisco_spokes     ### List of configured devices, located in hosts.py
##############################

save()

