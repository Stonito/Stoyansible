import diffios
from netmiko import ConnectHandler
import getpass

### Returns True if the config has been changed and False if it stays the same
def ChangedConfig(beforeConfig, afterConfig):
    ignore = "Stoyansible\Huawei\huawei_ignore.txt"
    diff = diffios.Compare(beforeConfig, afterConfig, ignore)
    exactConfigResult = "--- baseline\n+++ comparison\n\n\n"

    return diff.delta() != exactConfigResult

### Sends ssh command list to group of hosts and returns a list containing information whether the configuration has been changed
def huawei_config(hostsToConfigure,cfg_list,hostStateChange):
    usr = input("Username: ")
    passwd = getpass.getpass()

    for host in hostsToConfigure:

        currentHost = {
            "host": host,
            "username": usr,
            "password": passwd,
            "device_type": "huawei",
            "global_delay_factor": 0.1,    
            "conn_timeout": 20                              
        }
        net_connect = ConnectHandler(**currentHost)

        beforeConfig = net_connect.send_command(
                "display current-configuration",read_timeout=30).split("\n")

        cfg_output = net_connect.send_config_set(cfg_list)
        print(cfg_output)

        afterConfig = net_connect.send_command(
                "display current-configuration",read_timeout=30).split("\n")

        if ChangedConfig(beforeConfig, afterConfig):
            hostStateChange[host] = "Changed"
        else:
            hostStateChange[host] = "OK"
        
        net_connect.disconnect()  
    return hostStateChange

### Saves the configuration of group of hosts and returns a list containing information whether the startup configuration has changed
def huawei_save(hostsToSave,hostStateChange):

    usr = input("Username: ")
    passwd = getpass.getpass()

    for host in hostsToSave:

        currentHost = {
            "host": host,
            "username": usr,
            "password": passwd,
            "device_type": "huawei",
            "global_delay_factor": 0.1,    
            "conn_timeout": 20                              
        }
        net_connect = ConnectHandler(**currentHost)
        beforeSave = net_connect.send_command(
                "display saved-configuration",read_timeout=30).split("\n")
        net_connect.save_config()
        afterSave = net_connect.send_command(
                "display saved-configuration",read_timeout=30).split("\n")
        
        if ChangedConfig(beforeSave, afterSave):
            hostStateChange[host] = "New configuration saved!"
        else:
            hostStateChange[host] = "Configuration saved (nothing changed)."

    return hostStateChange