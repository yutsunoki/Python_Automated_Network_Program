#! /bin/python3
#
# import the netmiko module
import sys
from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException
from netmiko import NetmikoAuthenticationException

# create a function for send command to the networking device
# also design a different condition for circumstance 
def send_cisco_command(device, commands, selection, rt, lt):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            if selection == "timing":
                for command in commands:
                    output = ssh.send_command_timing(command,
                                                         strip_command=False,
                                                         strip_prompt=False,
                                                         read_timeout=rt,
                                                         last_read=lt
                                                     )
                    print(output, flush=True, end="\n", sep=" ")
                    if "bytes copied" in output:
                        print ("backup successfully")
            elif selection == "command":
                for command in commands:
                    output = ssh.send_command(command,
                                                 strip_command=False,
                                                 strip_prompt=False,
                                                 read_timeout=rt,
                                             )
                    print(output, flush=True, end="\n", sep=" ")
                    if "bytes copied" in output:
                        print ("backup successfully")
            elif selection == "config":
                output = ssh.send_config_set(commands,
                                                 strip_command=False,
                                                 strip_prompt=False,
                                                 read_timeout=rt,
                                             )
                print(output, flush=True, end="\n", sep=" ")
            else:
                print("no selection")
            ssh.disconnect()

        return 0
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

# starting
if __name__ == "__main__":

# assign networking devices information
    s0 = {
        "device_type" : "cisco_ios",
        "host" : "192.168.10.10",
        "username" : "s0",
        "password" : "cisco",
        "secret" : "cisco",
        "port" : 22,
    }
    r0 = {
        "device_type" : "cisco_ios",
        "host" : "192.168.10.1",
        "username" : "r0",
        "password" : "cisco",
        "secret" : "cisco",
        "port" : 22,
    }
    f0 = {
        "device_type" : "cisco_asa",
        "host" : "192.168.243.1",
        "username" : "f00",
        "password" : "cisco",
    }

# group for networking devices
    switch = s0
    router = r0
    firewall = f0

    devices = [s0,r0,f0]
    devices_name = ["s0","r0","f0"]

# configure automated commands for switch
    select = "config"
    commands = [
        "vlan 11",
            "name another",
        "int gi 0/0",
            "switchport trunk encapsulation dot1q",
            "switchport mode trunk",
        "int gi 0/1",
            "switchport mode access",
            "switchport access vlan 1",
        "int gi 0/2",
            "switchport mode access",
            "switchport access vlan 11",
    ]
#execute with the function
    send_cisco_command(switch,commands,select,0,0)

# configure automated commands for router
    select = "config"
    commands = [
        "int gi0/1.11",
            "encapsulation dot1Q 11",
            "ip addr 192.168.193.1  255.255.255.0",
            "no shut",
        "ip dhcp excluded-address 192.168.10.1",
        "ip dhcp pool private1",
            "network 192.168.10.0 255.255.255.0",
            "default-router 192.168.10.1",
        "ip dhcp excluded-address 192.168.193.1",
        "ip dhcp pool private2",
            "network 192.168.193.0 255.255.255.0",
            "default-router 192.168.193.1",
    ]
    send_cisco_command(router,commands,select,0,0)

# configure automated commands for firewall
    select = "config"
    commands = [
        "object network dmz-net",
            "host 172.30.0.2",
        "object network inside-net",
            "subnet 192.168.0.0 255.255.0.0",
            "nat (inside,outside) dynamic interface",
        "access-list inside-acl extended permit ip any any",
        "access-list dmz-acl extended permit ip any any",
        "access-list outside-acl extended permit ip any any",
        "access-group inside-acl in interface inside",
        "access-group dmz-acl global",
        "access-group outside-acl out interface outside",
    ]
    send_cisco_command(firewall,commands,select,10,0)

# send show command for networking devices
    select = "command"
    send_cisco_command(s0,["sh ip int br"],select,10,0)
    send_cisco_command(r0,["sh ip int br"],select,10,0)
    send_cisco_command(f0,["sh int ip br"],select,10,0)

# backup for networking devices
    select = "timing"
    tftpIP = "172.30.0.2"
    for deviceLists,Dname in zip(devices, devices_name):
        send_cisco_command(deviceLists,[f"copy run tftp://{tftpIP}/{Dname}","\r","\r","\r"],select,30,0)
