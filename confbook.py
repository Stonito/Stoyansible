"""
confbook.py

Sends configuration lines over SSH to a list of hosts and returns the state of the made changes

"""

import hosts
from IOS.ios import ios_config
from termcolor import colored

def config(configFile):

    cfg_list = open(configFile).readlines()
    hostStateChange = {}

    if platform == "ios":
        hostStateChange = ios_config(hostsToConfigure,cfg_list,hostStateChange)
    else:
        pass
    
    print("\nCommands run:")
    for line in cfg_list:
        print(colored(line, 'cyan'))
    for host,state in hostStateChange.items():
        if state == "Changed":
         print(colored(f"{host} : {state}", 'yellow'))
        else:
            print(colored(f"{host} : {state}", 'green'))

### Admin-defined variables
##############################
platform = "ios"    ### Platform of configured devices - ios, huawei, mikrotik, etc.
hostsToConfigure = hosts.cisco_spokes   ### List of configured devices, located in hosts.py
configFile = "Stoyansible\IOS\Configs\playbook_ios.txt"     ### Path to configuration file
##############################

config(configFile)
