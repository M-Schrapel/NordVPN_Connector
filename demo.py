#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Schrapel

@description: A demo of the VPN connector for NordVPN on Debian. In addition VPN creates an overview of connectable VPN's.

@info: Tested on Raspberian with an Raspberry Pi 4
@license: MIT
"""
from VPN import *

#### Testcases:
    
## credentials are stored as files
## for security reasons I recommend not using variables in python
## set credentials in the vpn_acc.txt from subfolder VPNdata once
user="<your_email>"
password="<your_password>"

## create vpn
v = VPN()
print("Your IP is: "+v.getIP())
## you only have to set credentials once!
## credentials are stored as files
v.setCredentials(user,password)
## connect to vpn server
v.rotate_vpn()
## connect VPN without retry in case of server connection errors
v.rotate_vpn(retry=False)
v.setVPNType("tcp")
v.rotate_vpn(retry=False)
v.setVPNType("udp")
## get stored regions
regions=v.getAllRegions()
## set new regions
v.setRegions(regions[0:2])
## connect again 
v.rotate_vpn()
## close vpn
v.close_vpn()
## alternative
v = VPN(regions=["us","fr","jp","de"])
v.rotate_vpn()
v.close_vpn()
print("\nYour IP is: "+v.getIP())