# dhcp_discover
DHCP client discovery information

```
python3 discovery_dhcp.py en0
# in your case, specify the interface on your local machine/server (eth0, ens192 etc..)
```

An example output should be:
```
* waiting for DHCPOFFER
* constructing DHCPDISCOVER packet
* sending DHCPDISCOVER...
* DHCPOFFER received:
ip offered = 192.168.0.129
message-type = 2
server_id = 192.168.0.1
lease_time = 7200
renewal_time = 3600
rebinding_time = 6300
subnet_mask = 255.255.255.0
broadcast_address = 192.168.0.255
name_server = 192.168.0.1
router = 192.168.0.1
```
