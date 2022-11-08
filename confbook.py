"""
confbook.py

Sends configuration lines over SSH to a list of hosts and returns the state of the made changes

"""

import hosts
from IOS.ios import ios_config
from Huawei.huawei import huawei_config
from termcolor import colored

### Admin-defined variables
##############################
platform = "huawei"    ### Platform of configured devices - ios, huawei, mikrotik, etc.
hostsToConfigure = hosts.huawei_devs   ### List of configured devices, located in hosts.py
configFile = "Stoyansible2.0\Huawei\Configs\config_acl_huawei.txt"     ### Path to configuration file
##############################

def main(platform,configFile,hostsToConfigure):

    cfg_list = open(configFile).readlines()
    hostStateChange = {}

    if platform == "ios":
        hostStateChange = ios_config(hostsToConfigure,cfg_list,hostStateChange)
    elif platform == "huawei":
        hostStateChange = huawei_config(hostsToConfigure,cfg_list,hostStateChange)
    else:
        pass
    
    print("\nCommands run:")
    print("================================")
    for line in cfg_list:
        print(colored(line.rstrip(), 'cyan'))
    print("================================")
    print("================================")
    print()
    for host,state in hostStateChange.items():
        if state == "Changed":
         print(colored(f"{host} : {state}", 'yellow'))
        else:
            print(colored(f"{host} : {state}", 'green'))

if __name__ == '__main__':
    main(platform,configFile,hostsToConfigure)