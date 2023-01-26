#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Schrapel

@description:   An example script you can run on startup of your computer to browse the net anonymously.
                Add this script to /etc/rc.local by adding python /path_to_file/startup.py
@info: Tested on Raspberian with an Raspberry Pi 4
@license: MIT
"""
import argparse
from VPN import *

# set parse arguments
parser = argparse.ArgumentParser(description='Set Region of VPNs, number of trials and verbose')
# region of VPN - when no info is given connection can be on any server
parser.add_argument("--region", type=str, default="")
# number of retries in case of errors
parser.add_argument("--maxtrials", type=int, default=25)
# suppress terminal output
parser.add_argument("--verbose", type=int, default=False)
# arguments are in args
args = parser.parse_args() 

vpn_ready=False # connection state
if args.region != "": # region in args
    if args.region in VPN().getAllRegions(): # proof if region exists
        # make VPN connection
        v = VPN(verbose=args.verbose,regions=[args.region])
        # establish connection
        vpn_ready = v.rotate_vpn(max_trials=args.maxtrials)

# in case of errors or no region was given
if not vpn_ready: # no connection established
    # make VPN connection
    v = VPN(verbose=args.verbose)
    # establish connection
    v.rotate_vpn(max_trials=args.maxtrials)
