# VPNdata Folder
This folder is created automatically when you create a VPN object. 
It contains your NordVPN account information in  *vpn_acc.txt* and the .csv log file *vpn_states.csv*.

## Account information
The file *vpn_acc.txt* contains your NordVPN account data.
**Don't share this file!**

```
<First Line is your account mail>
<Second Line is your account password>
```

## Log file
The file *vpn_states.csv* logs your VPN connections.
Sometimes the servers are not available. For example, you can use your log data to identify the most reliable VPN servers.


| Name of VPN | VPN filename | Recent VPN state | Timestamps | VPN state history |
|---|---|---|---|---|
| example0 | example0.nordvpn.com.udp.ovpn | False | {'01/01/1970, 00:00:00'} | [False] |
| ... | ... | ... | ... | ... |
