import diffios
from netmiko import ConnectHandler
import getpass

### Returns True if the config has been changed and False if it stays the same
def ChangedConfig(beforeConfig, afterConfig):
    ignore = "Stoyansible\IOS\ignore.txt"
    diff = diffios.Compare(beforeConfig, afterConfig, ignore)
    exactConfigResult = "--- baseline\n+++ comparison\n\n\n"

    return diff.delta() != exactConfigResult

### Sends ssh command list to group of hosts and returns a list containing information whether the configuration has been changed
def ios_config(hostsToConfigure,cfg_list,hostStateChange):

    usr = input("Username: ")
    passwd = getpass.getpass()

    for host in hostsToConfigure:

        net_connect = ConnectHandler(
            device_type="cisco_xe",
            host=host,
            username=usr,
            password=passwd,
        )
        beforeConfig = net_connect.send_command(
                "show run").split("\n")

        cfg_output = net_connect.send_config_set(cfg_list)
        print(cfg_output)

        afterConfig = net_connect.send_command(
                "show run").split("\n")

        if ChangedConfig(beforeConfig, afterConfig):
            hostStateChange[host] = "Changed"
        else:
            hostStateChange[host] = "OK"

    return hostStateChange

### Saves the configuration of group of hosts and returns a list containing information whether the startup configuration has changed
def ios_save(hostsToSave,hostStateChange):

    usr = input("Username: ")
    passwd = getpass.getpass()

    for host in hostsToSave:

        net_connect = ConnectHandler(
            device_type="cisco_xe",
            host=host,
            username=usr,
            password=passwd,
        )
        beforeSave = net_connect.send_command(
                "show startup-config").split("\n")
        net_connect.save_config()
        afterSave = net_connect.send_command(
                "show startup-config").split("\n")
        
        if ChangedConfig(beforeSave, afterSave):
            hostStateChange[host] = "New configuration saved!"
        else:
            hostStateChange[host] = "Configuration saved (nothing changed)."

    return hostStateChange