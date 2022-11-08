"""
savebook.py

Saves the configuration of list of given hosts and returns state of the made changes

"""

import hosts
from IOS.ios import ios_save
from Huawei.huawei import huawei_save
from termcolor import colored

### Admin-defined variables
##############################
platform = "huawei"    ### Platform of configured devices - ios, huawei, mikrotik, etc.
hostsToSave = hosts.huawei_dev     ### List of configured devices, located in hosts.py
##############################

def main(platform,hostsToSave):
    hostStateChange= {}

    if platform == "ios":
        hostStateChange = ios_save(hostsToSave, hostStateChange)
    elif platform == "huawei":
        hostStateChange = huawei_save(hostsToSave, hostStateChange)
    else:
        pass

    for host,state in hostStateChange.items():
        if state == "Changed":
            print(colored(f"{host} : Configuration saved!", 'yellow'))
        else:
            print(colored(f"{host} : OK", 'green'))

if __name__ == '__main__':
    main(platform,hostsToSave)

