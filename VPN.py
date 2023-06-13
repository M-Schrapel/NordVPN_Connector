#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maximilian Schrapel

@description: A VPN connector for NordVPN on Debian.

@license: MIT
"""
import signal                    #process signals
import os                        # paths and files
import subprocess                # terminal
from time import sleep           # timestamps
from random import randrange     # random file selection
from warnings import warn        # warning messages
import pandas as pd              # handling .csv log files
from datetime import datetime    # timestamps
from shutil import which         #find paths
import urllib.request            #getIP

"""A VPN handler for NordVPN using OpenVPN on Debian

:param regions: Regions, if empty all regions will be used
:type regions: list[str]
:param vpn_folder: VPN folder without tcp or udp at the end, works with default installations
:type vpn_folder: str
:param vpn_type: VPN connection type (udp or tcp), use udp as recommended by NordVPN
:type vpn_type: str
:param ovpn_folder: openVPN folder
:type vpn_type: str
:param vpn_csvfolder: folder for storing connectivity logs and account information
:type vpn_csvfolder: str
:param vpn_csv: .csv file for storing connectivity states
:type vpn_csv: str
:param vpn_file: file with your NordVPN account and password
:type vpn_file: str
:param make_vpnlist: when True the script creates a .csv file with connectable VPN servers
:type make_vpnlist: bool
:param verbose: print information on terminal
:type verbose: bool

@author: Maximilian Schrapel
@license: MIT
"""

class VPN:
    def __init__(self,
                 regions=[],
                 vpn_folder="/etc/openvpn/ovpn_",
                 vpn_type="udp",
                 ovpn_folder="/etc/init.d/openvpn",
                 vpn_csvfolder="VPNdata",
                 vpn_file="vpn_acc.txt",
                 vpn_csv="vpn_states.csv",
                 make_vpnlist=True,
                 verbose=True,
                 sleep_time=2,
                 connect_retry_max=1, 
                 server_poll_timeout=3
                 ):
        self.__regions=regions
        self.vpn_folder=vpn_folder
        self.ovpn_folder=ovpn_folder
        self.vpn_csvfolder=vpn_csvfolder
        self.vpn_csv=vpn_csv
        self.__vpn_file=vpn_file
        self.vpn_type=vpn_type
        self.make_vpnlist=make_vpnlist
        self.verbose=verbose
        self.servers=[]
        self.init_vpn()
        self.last_vpn=[]
        self.connected=False
        self.sleep_time=sleep_time
        self.connect_retry_max=connect_retry_max, 
        self.server_poll_timeout=server_poll_timeout
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)  
        signal.signal(signal.SIGCONT, signal.SIG_IGN) 
        
    # Set regions with list of strings e.g. ['us','fr','de']
    def setRegions(self,regions):
        ret = True
        if type(regions)==str:# if string was given
            regions=[regions]
            
        if len(regions)>0 and type(regions)==list:
            rems=[]# list of not available regions in regions
            all_regions=self.getAllRegions()
            for r in regions: # check regions
                if type(r)!=str:
                    ret = False
                    break
                if not r in all_regions: # region not available
                    rems.append(r)
                    if self.verbose:
                        print("Region "+r+" is not available!")
            if len(rems)>0:
                for rm in rems:
                    regions.remove(rm)
        else:
            if type(regions)!=str:
                ret = False
        if len(regions)==0:
            return False
        if not ret:
            if self.verbose:
                print("Only strings are allowed!")
        else:
            self.init_vpn(regions=regions)
        return ret
        
    # Set UDP or TCP server connection
    def setVPNType(self,type_vpn):
        # to lower case!
        type_vpn = type_vpn.lower()
        if type_vpn=="udp" or type_vpn=="tcp":
            self.vpn_type=type_vpn
            self.init_vpn()
            return True
        else:
            if self.verbose:
                print("Only udp or tcp allowed!")
            return False
        
    # returns all available regions from NordVPN in a list
    def getAllRegions(self):
        targets = next(os.walk(self.vpn_folder+self.vpn_type), (None, None, []))[2] 
        ret=[]
        for i in range(0,len(targets)):
            t="".join([j for j in targets[i][:targets[i].find(".nordvpn")] if not j.isdigit()])
            if not t in ret:
                ret.append(t)
        return ret
    
    # set account information of NordVPN
    def setCredentials(self,user,password):
        userfolder=os.path.join(self.vpn_csvfolder,self.__vpn_file)
        if not os.path.exists(userfolder):
            if not os.path.exists(self.vpn_csvfolder):
                os.mkdir(self.vpn_csvfolder)
        f = open(userfolder, "w")
        f.write(user+"\n"+password)
        f.close()
        
    # initialize vpn connection
    def init_vpn(self,regions=[]):
        if regions!=[]:
            self.__regions= regions
        self.servers = self.getVPNs(regions=regions)
        userfolder=os.path.join(self.vpn_csvfolder,self.__vpn_file)
        if not os.path.exists(userfolder):
            warn("You have to add your credentials to: "+userfolder+"\nAlternatively use setCredentials(<user>,<pass>)")

            
    # get vpn servers within desired regions
    def getVPNs(self,regions=[]):
        if regions!=[]:
            self.__regions= regions
        targets=[]
        if self.__regions != []: # list of regions
            for region in self.__regions:
                if targets == []:
                    targets = self.make_target_servers(region=region)
                else:
                    targets.extend(self.make_target_servers(region=region))
        else: # all regions
            targets = next(os.walk(self.vpn_folder+self.vpn_type), (None, None, []))[2] 
            self.__regions=self.getAllRegions()
        return targets
    
    # get all VPN servers within a given country
    def make_target_servers(self,region=[]):
        # read folder
        filenames = next(os.walk(self.vpn_folder+self.vpn_type), (None, None, []))[2]
        
        servers=[]
        for file in filenames:
            if ".nordvpn.com."+self.vpn_type+".ovpn" in file: # add region VPN's
                if file[0:2] == region or region =="all" or region == []:
                    servers.append(file)
        return servers
    
    # close vpn connection
    def close_vpn(self):
        if self.verbose:
            print("CLosing VPN ... \n")
        subprocess.run(["sudo", "/usr/bin/killall" ,"openvpn"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #Wait for OS network config to be restored
        sleep(self.sleep_time)
        
    # get current public IP
    def getIP(self):
        return  urllib.request.urlopen("https://ident.me").read().decode("utf8")

    #Handler for receive SIGCHILD signal from openvpn process 
    def SIGCHILD_handler(self, _, __):
        if self.verbose:
            print('SIGCHILD received --> Connection failed')
        self.connected = False

    #Handler for receive SIGCONT signal, triggered by openvpn when a successfull TUN/TAP interface has been made. Specified by '--up' option.
    def SIGCONT_handler(self, _, __):
        if self.verbose:
            print('SIGCONT received --> Connection successfull')
        self.connected = True

    # Use another randomly selected VPN
    def rotate_vpn(self,trials=0, retry=True,max_trials=10):
        res=False
        self.close_vpn()
        # select random VPN
        file_vpn = self.servers[randrange(0,len(self.servers)-1)]
        # credentials
        userfolder=os.path.join(self.vpn_csvfolder,self.__vpn_file)
        if not os.path.exists(userfolder):
            warn("You have to add your credentials to: "+userfolder+"\nAlternatively use setCredentials(<user>,<pass>)")
        vpn_csvfolder=self.vpn_csvfolder
        # .csv log file
        vpn_list=os.path.join(vpn_csvfolder, self.vpn_csv)

        """ Initiate VPN connection"""
        #Get PID which receive the SIGCONT signal
        ppid = os.getpid()
        #Build the openvpn command line 
        python_path = which("python3")
        openvpn_path = which("openvpn")
        
        up_cmd = python_path + " -c \'from os import kill; kill("+str(ppid)+","+str(int(signal.SIGCONT)) +")\'"
        cmd_start = ['sudo', openvpn_path, '--connect-retry-max', str(self.connect_retry_max), '--tls-exit', '--server-poll-timeout', str(self.server_poll_timeout), '--script-security', '2', '--up', up_cmd, '--auth-nocache', '--config', os.path.join(self.vpn_folder+self.vpn_type,file_vpn), '--auth-user-pass', userfolder]
        if self.verbose:
            print("Connecting ...")    
        #Update handlers for SIGCHLD and SIGONT signals : 
        signal.signal(signal.SIGCHLD, self.SIGCHILD_handler)  
        signal.signal(signal.SIGCONT, self.SIGCONT_handler) 
        #Redirect stdout to a file for debugging
        stdout = open('stdout.txt', 'w')
        subprocess.Popen(cmd_start, stdout=stdout, stderr=subprocess.PIPE)
        #Waiting for signal SIGCONT if success or SICHILD if fail
        signal.pause()
        #Ignore signals until next connection
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)  
        signal.signal(signal.SIGCONT, signal.SIG_IGN) 

        """Post VPN connection process"""
        #Wait for OS network config finished and update the IP
        sleep(self.sleep_time)
        ip = self.getIP()
        # connection was not successful
        if self.connected == False:
            if self.verbose:
                print(file_vpn.replace('.nordvpn.com.'+self.vpn_type+'.ovpn','')+" VPN error - IP: "+ip.replace("\n",""))
            if self.make_vpnlist:
                self.vpnlist(file_vpn,False,vpn_list)
            if retry:
                trials+=1
                if trials==max_trials: # no connection?
                    if self.verbose:
                        print("Connections not succeded, max_trials reached")
                else:
                    self.rotate_vpn(trials=trials, max_trials=max_trials)
        else: 
            self.last_vpn=file_vpn
            if self.verbose:
                print(file_vpn.replace('.nordvpn.com.'+self.vpn_type+'.ovpn','')+" VPN IP: "+ip.replace("\n",""))
            if self.make_vpnlist:
                self.vpnlist(file_vpn,True,vpn_list)
            res=True
        return res

        
    # Add VPN connection to overview in .csv log file
    def vpnlist(self, file_vpn, good_vpn = True,vpn_list=[]):
        if vpn_list==[]:
            vpn_list=os.path.join(self.vpn_csvfolder,self.__vpn_file)
        # df = False
        name = file_vpn.replace(".nordvpn.com."+self.vpn_type+".ovpn","")
        # .csv log file structure
        data_vpn ={
            'Name':name,                                            # name of VPN server
            'VPN': file_vpn,                                        # filename of VPN server
            'Works':good_vpn,                                       # connection status
            'Time':{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}, # timestamp
            'History':[good_vpn]}                                   # history of connection states
        
        if not os.path.exists(vpn_list): # proof if file exists
            if self.vpn_csvfolder in vpn_list:
                if not os.path.exists(self.vpn_csvfolder):
                    os.mkdir(self.vpn_csvfolder)
            df = pd.DataFrame([data_vpn])
            df.to_csv(vpn_list,index=False)
        else:
            df = pd.read_csv(vpn_list)
            if not file_vpn in list(df["VPN"]): # new connected VPN
                df = pd.concat([df,pd.DataFrame([data_vpn])]) 
            else: # VPN has been selected before
                # row
                indx=df.where(df["VPN"]==file_vpn)["Time"].dropna().index.tolist()[0]
                # VPN works?
                df.at[indx,"Works"]=good_vpn
                # timestamp
                t_cell=df.at[indx,"Time"]
                t_cell=t_cell[:-1]+","+str(data_vpn["Time"])[1:]
                # status history
                h_cell=df.at[indx,"History"]
                h_cell=h_cell[:-1]+","+str(good_vpn)+h_cell[-1]
                # set values
                df.at[indx,"Time"]=t_cell
                df.at[indx,"History"]=h_cell
            df.to_csv(vpn_list,index=False) # save .csv log file
