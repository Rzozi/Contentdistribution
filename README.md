Content distribution Over SDN 



    This code is a first try to implement an API for a content distribution service over SDN. 
    
    


-->Rebooting steps:

- up virtual network interface
root@server:~# ip tuntap add mode tap vnet1
root@server:~# ip link set vnet1 up

- (repeat for other virtual network interfaces, for example of vnet2)
root@server:~# ip tuntap add mode tap vnet2
root@server:~# ip link set vnet2 up

- up bridge and bridged interface
root@server:~# ifconfig eth0 0 up
root@server:~# cd ./openvswitch/datapath/linux; modprobe openvswitch;cd ~;/root/openvswitch.sh  
root@server:~# ifconfig br0 192.168.1.20 netmask 255.255.255.0 up

- run floodlight
root@server:~# cd /root/floodlight; java -jar target/floodlight.jar


--> Static flow definition:


curl -X POST -d '{"switch":"00:00:30:f9:ed:c6:a3:46", "name":"static-flow3", " cookie":"0", "priority":"32768", "ipv4_src":"192.168.1.24", "eth_type":"0x0800","active":"true","actions":"output=5"}' http://localhost:8080/wm/staticflowpusher/json


Config Floodlight/Openvswitch : http://dannykim.me/danny/openflow/57620?ckattempt=1

