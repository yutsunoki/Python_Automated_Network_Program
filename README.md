# Python_Automated_Network_Program

This is my practical about the automated network program with python.

```
# show ip route
root@eve-ng:~# ip route
default via 192.168.0.1 dev pnetd
192.168.0.0/24 dev pnet0 proto kernel scope link src 192.168.0.8

# setup ip route and expose ip for eve-ng emulated device
ip route add 192.168.0.0/16 dev pnet0 proto kernel scope link src 192.168.0.8
ip route add 172.30.0.0/16 dev pnet0 via 192.168.10.1
ip route add 10.0.0.0/8 dev pnet0 via 192.168.10.1

# show ip route
root@eve-ng:~# ip route
192.168.0.1 dev pnetd
10.0.0.0/8 via 192.168.10.1 dev pnetd
172.30.0.0/16 via 192.168.10.1 dev pnetd
192.168.0.0/24 dev pnet0 proto kernel scope link src 192.168.0.8
192.168.0.0/16 dev pnet0 proto kernel scope link src 192.168.0.8
```

![planing_map](img/planing_map.png)
