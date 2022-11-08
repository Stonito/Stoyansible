import diffios
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoAuthenticationException, NetMikoTimeoutException
import getpass
import threading
from queue import Queue
from art import *
from termcolor import colored

hostsQueue = Queue()
print_lock = threading.Lock()

### Returns True if the config has been changed and False if it stays the same
def ChangedConfig(beforeConfig, afterConfig):
    ignore = "Stoyansible2.0\Huawei\huawei_ignore.txt"
    diff = diffios.Compare(beforeConfig, afterConfig, ignore)
    exactConfigResult = "--- baseline\n+++ comparison\n\n\n"

    return diff.delta() != exactConfigResult

### Function used in threads to connect to hosts
def deviceConnector(i,usr,passwd,cfg_list,hostStateChange):

    # This while loop runs indefinitely and grabs IP addresses from the queue and processes them
    # Loop will stop and restart if "ip = q.get()" is empty
    while True:
        hostIP = hostsQueue.get()
        currentHost =  {
            'host': hostIP,
            'username': usr,
            'password': passwd,
            'device_type': 'huawei',
            'global_delay_factor': 0.1,
            'conn_timeout': 20
        }

        net_connect = ConnectHandler(**currentHost)
        with print_lock:
            print(colored("Connected to: {}".format(hostIP), 'green'))

        if cfg_list == "saveconfig":
            beforeConfig = net_connect.send_command(
                "display saved-configuration",read_timeout=30).split("\n")
            net_connect.save_config()
            afterConfig = net_connect.send_command(
                "display saved-configuration",read_timeout=30).split("\n")
        else:
            beforeConfig = net_connect.send_command(
                "display current-configuration",read_timeout=30).split("\n")
            cfg_output = net_connect.send_config_set(cfg_list)
            print(cfg_output)
            afterConfig = net_connect.send_command(
                "display current-configuration",read_timeout=30).split("\n")

        if ChangedConfig(beforeConfig, afterConfig):
            hostStateChange[hostIP] = "Changed"
        else:
            hostStateChange[hostIP] = "OK"

        net_connect.disconnect
        hostsQueue.task_done()

### Sends ssh command list to group of hosts and returns a list containing information whether the configuration has been changed
def huawei_config(hostsToConfigure,cfg_list,hostStateChange):
    usr = input("Username: ")
    passwd = getpass.getpass()
    print()
    print(">>>>>>>>>>>>>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>>>>")

    # Setting up threads based on number of hosts
    for i in range(len(hostsToConfigure)):
        thread = threading.Thread(target=deviceConnector, args=(i,usr,passwd,cfg_list,hostStateChange,))
        thread.setDaemon(True)
        thread.start()

    # For each host add its IP address to the queue
    for hostIP in hostsToConfigure:
        hostsQueue.put(hostIP)

    # Wait for all tasks in the queue to be marked as completed (task_done)
    hostsQueue.join()
    print("\n====================")
    print("Playbook complete")
    print("====================\n")

    return hostStateChange

### Saves the configuration of group of hosts and returns a list containing information whether the startup configuration has changed
def huawei_save(hostsToSave,hostStateChange):

    tprint("Stoyansible")

    usr = input("Username: ")
    passwd = getpass.getpass()
    cfg_list = "saveconfig"
    print()
    print(">>>>>>>>>>>>>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>>>>")
    
    for i in range(len(hostsToSave)):
        thread = threading.Thread(target=deviceConnector, args=(i,usr,passwd,cfg_list,hostStateChange,))
        thread.setDaemon(True)
        thread.start()

    for hostIP in hostsToSave:
        hostsQueue.put(hostIP)

    hostsQueue.join()
    print("\n====================")
    print("Playbook complete")
    print("====================\n")

    return hostStateChange