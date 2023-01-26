# VPNdata Folder
This folder will be automatically created when creating an VPN object.
It holds your NordVPN account information in *vpn_acc.txt* and the .csv log files *vpn_states.csv*.

## Account information
The file *vpn_acc.txt* holds your NordVPN account data.
Don't share this file! 

    ```
    <First Line is your account mail>
    <Second Line is your account password>
    ```
    
## Log file
The file *vpn_states.csv* logs your VPN connections.
Sometimes servers are not available. You can use your log data e.g. to identify the most reliable VPN servers.


| Name of VPN | VPN filename | Recent VPN state | Timestamps | VPN state history |
|---|---|---|---|---|
| example0 | example0.nordvpn.com.udp.ovpn | False | {'01/01/1970, 00:00:00'} | [False] |
| ... | ... | ... | ... | ... |
