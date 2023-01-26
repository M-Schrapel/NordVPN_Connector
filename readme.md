# NordVPN Connector for Python 3 on Debian
This project makes it easy and efficient to connect to a NordVPN server using OpenVPN and Python3 on Debian.
In addition, you can create a log .csv-file of working VPN servers and select a desired region.
Another advantage for tiny devices like Raspberry Pi is that this project doesn't require many CPU or memory resources and is easy to run from a terminal. 
**You can automatically connect to a VPN on start of your computer and browse the internet anonymously!** 
*(NordVPN account is required!)*

## Contents
- [Setup](#setup)
- [Required Python packages](#required-python-packages)
- [Settings](#settings)
	- [UDP & TCP](#udp-&-tcp-vpn-servers)
	- [Regional VPN's](#regional-vpn-servers)
	- [Connect & Rotate VPN's](#connect-&-rotate-vpn-servers)
	- [Close VPN connection](#close-vpn-connection)
	- [Log Files](#log-files)
	- [Verbose output](#verbose-output)
	- [Get public IP](#get-your-public-ip)
- [Startup script](#startup-script)
	- [Setup script](#setup-script)
	- [Parameters](#additional-params)
- [License](#license)

## Setup

1. To install OpenVPN (required!), follow the instructions by NordVPN [here](https://support.nordvpn.com/Connectivity/Linux/1047409422/Connect-to-NordVPN-using-Linux-Terminal.htm) 
2. Install *dnsutils* using the command:
    ```
    $ sudo apt-get install dnsutils 
    ```
3. Download this repository
4. Open the terminal and navigate to the downloaded directory
5. Optional: Install requirements using the command (see [packages](#required-python-packages) for details):
    ```
    $ pip install -r requirements.txt
    ```
6. Open the the file [demo.py]() and add your NordVPN credentials on Line 18 & 19
    ```python
    user="<your_email>"
    password="<your_password>"
    ```
    **!For security reasons I recommend not using variables with account information in Python!**
    **Better Solution**: Comment out or delete Line 25 in [demo.py]() and add your NordVPN credentials in [VPNdata/vpn_acc.txt]():
    ```
    <First Line is your account mail>
    <Second Line is your account password>
    ```
    Internally, the program uses files and the *--auth-user-pass* functionality of OpenVPN to make logins as secure as possible.
7. Run the [demo.py]() file using python 3
    ```
    $ python demo.py
    ```
8. When you see after some trials similar output on the terminal: 
    ```
    Your IP is: xxx.xxx.xxx.xxx
    <VPN Server Name> VPN IP: xxx.xxx.xxx.xxx
    ```
    Congratulations! You successfully connected to an NordVPN server! 
9. When you only see similar output to this: 
    ```
    <VPN Server Name> VPN error - IP: xxx.xxx.xxx.xxx
    ```
    Please check your account name and password in Step 6. 
    If you still have problems go back to 1.

## Required Python packages
Please ensure you have installed the following Python3 packages:
- os
- subprocess
- time
- random
- warnings
- pandas
- numpy
- datetime
- argparse

Go to [Setup](#setup) Step 4. and 5. to install dependencies


## Settings
Some additional functionality makes this project more universal and easy to use in your Python projects. 
### UDP & TCP VPN Servers
Use the method *setVPNType()* to use TCP or UDP servers.
```python
from VPN import *       # import VPN class
v = VPN()               # use UDP servers by default
v.setVPNType("tcp")     # use TCP servers
v.setVPNType("udp")     # use UDP servers
```
This project uses UDP VPN servers because of fast but less reliable transmissions by default.
Further information can be found [here](https://nordvpn.com/de/blog/tcp-or-udp-which-is-better/).

### Regional VPN Servers
Use the method *setRegions()* to use VPN servers within an country area.
To get all available regions use the method *getAllRegions()* 
```python
v = VPN()                           # create VPN object
regions=v.getAllRegions()           # returns a list of all available regions
v.setRegions(["us","de","fr"])      # "us" = USA, "de" = Germany, "fr" = France
v.setRegions("jp")                  # works with only one region. returns False when not available
```
To get a list of available servers within a region use the method *getVPNs()*
```python
v = VPN(regions=["uk"])             # only use VPN servers in UK
print(v.getVPNs())                  # will print all servers in UK
print(v.getVPNs(["us","de","fr"]))  # will print all servers in the USA, Germany and France
```

### Connect & Rotate VPN Servers
To connect an VPN server use the method *rotate_vpn()*.
It will automatically try to reconnect unless you secified the *retry=False* parameter.
Furthermore, you can configure the maximum trials by by the *max_trials=10* parameter. 
The method *rotate_vpn()* returns *True* in case of successful connections.
```python
v = VPN()
v.rotate_vpn()              # selects a random VPN from all VPN's
v.rotate_vpn(retry=False)   # will only try to connect once and returns True or False
v.rotate_vpn(max_trials=10) # will try 10 times to estabilsh a connection in case of errors

if VPN().rotate_vpn():      # works as well 
    print("connected!")
VPN().close_vpn()           
```

### Close VPN connection
To disconnect from an VPN server use the method *close_vpn()*.
```python
v = VPN()
v.rotate_vpn()  # connect to a VPN server
v.close_vpn()   # close all OpenVPN connections
```
### Log Files
Initially, all Log files will be stored in the subfolder VPNdata as *vpn_states.csv*.
However, if you prefer not to store any logs change the parameter *make_vpnlist* to *False*.
Furthermore, you can change the subfolder *VPNdata* and name of the stored Log file *vpn_acc.txt*:
To store your log files and credentials in a different folder, change the folder to *vpn_csvfolder=""* and add your path to the files *vpn_csv="/path/vpn_states.csv"* and *vpn_file="/path/vpn_acc2.txt"*.

```python
v = VPN(make_vpnlist=False,         # create no log file
        vpn_csvfolder="VPNdata2",   # change folder of log file
        vpn_file="vpn_acc2.txt",    # change credential information file in folder VPNdata2
        vpn_csv="vpn_states2.csv")  # change target .csv log file
v.make_vpnlist=True                 # create log file (default=True)
```
The .csv log file contains the list of connected VPN servers, their current state and timestamps of connection trials.

### Verbose output
By default VPN prints all information including connection states on your terminal.
In case you want to suppress information on terminal set the parameter *verbose = False*:
```python
v = VPN(verbose=True)   # by default all information is printed on your terminal             
v.verbose=False         # suppress most print output
```

### Get your public IP
To get your current public IP use *getIP()*:
```python
print(VPN().getIP())    # prints your public IP as string
```

## Startup script
To automatically connect to a VPN server when on start of your PC, you can use the included scripts.
### Setup Script
First, check if you have *argparse* for python installed. Run the script [connectVPN.py]():
```
$ python /path_to_this_repository/connectVPN.py
```
Your public IP will be changed now. You can check this [here](https://whatismyipaddress.com/).

Now, open your terminal and type:
```
$ sudo nano /etc/rc.local
```
Add the line to the file with the path to this directory:
```
$ python /path_to_this_repository/connectVPN.py
```
Save the script by pressing <kbd>Ctrl</kbd> + <kbd>o</kbd> and then press <kbd>Enter</kbd>.
After rebooting your PC, you will be automatically connected to a VPN. 
### Additional Params
In addition, you can set a region for your VPN by passing the argument *region* and a desired country (here *uk*):
```
$ python /path_to_this_repository/connectVPN.py --region uk
```
Congratulations! You can now browse anonymously on start.
To disconnect you can run this simple script:
```
$ python /path_to_this_repository/disconnectVPN.py
```
Furthermore, you can create executeable bash scripts on your Desktop for easy use.


## License
This repository is provided by Maximilian Schrapel under MIT license. For inquiries, feel free to contact me.