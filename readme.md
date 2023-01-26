# NordVPN Connector for Python 3 on Debian
This project makes it easy and efficient to connect to a NordVPN server using OpenVPN and Python3 on Debian.
In addition, you can create a .csv file of working VPN servers and select a desired region.
Another advantage for small devices like the Raspberry Pi is that this project does not require a lot of CPU or memory resources and can be easily started from a terminal. 
**You can automatically connect to a VPN when you start your computer and surf the internet anonymously!**
*(NordVPN account is required!)*

## Contents
- [Setup](#setup)
- [Required Python packages](#required-python-packages)
- [Settings](#settings)
	- [Connect & Rotate VPN's](#connect-and-rotate-vpn-servers)
	- [Close VPN connection](#close-vpn-connection)
	- [UDP & TCP](#udp-and-tcp-vpn-servers)
	- [Regional VPN's](#regional-vpn-servers)
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
6. Open the the file [demo.py](https://github.com/M-Schrapel/NordVPN_Connector/blob/main/demo.py) and add your NordVPN credentials on Line 18 & 19
    ```python
    user="<your_email>"
    password="<your_password>"
    ```
    **!For security reasons I recommend not using variables with account information in Python!**
    **Better Solution**: Comment out or delete Line 25 in [demo.py](https://github.com/M-Schrapel/NordVPN_Connector/blob/main/demo.py) and add your NordVPN credentials in [VPNdata/vpn_acc.txt](https://github.com/M-Schrapel/NordVPN_Connector/blob/main/VPNdata/vpn_acc.txt):
    ```
    <First Line is your account mail>
    <Second Line is your account password>
    ```
    Internally, the program uses files and the *--auth-user-pass* functionality of OpenVPN to make logins as secure as possible.
7. Run the [demo.py](https://github.com/M-Schrapel/NordVPN_Connector/blob/main/demo.py) file using python 3
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
Some additional features make this project more universal and easier to use in your Python projects.

### Connect and Rotate VPN Servers
To connect to a VPN server, use the *rotate_vpn()* method.
It will automatically try to reconnect unless you have set the parameter *retry=False*.
You can also set the maximum number of attempts with the parameter *max_trials=10*. 
The *rotate_vpn()* method returns *True* if a connection was successful.
```python
from VPN import *           # import VPN class
v = VPN()
v.rotate_vpn()              # selects a random VPN from all VPN's
v.rotate_vpn(retry=False)   # will only try to connect once and returns True or False
v.rotate_vpn(max_trials=10) # will try 10 times to estabilsh a connection in case of errors

if VPN().rotate_vpn():      # works as well 
    print("connected!")
VPN().close_vpn()           
```

### Close VPN connection
To disconnect from a VPN server, use the *close_vpn()* method.
```python
v = VPN()
v.rotate_vpn()  # connect to a VPN server
v.close_vpn()   # close all OpenVPN connections
```

### UDP and TCP VPN Servers
Use the method *setVPNType()* to use TCP or UDP servers.
```python
v = VPN()               # use UDP servers by default
v.setVPNType("tcp")     # use TCP servers
v.setVPNType("udp")     # use UDP servers
```
This project uses UDP VPN servers by default because of their fast but less reliable transmissions.
Further information can be found [here](https://nordvpn.com/de/blog/tcp-or-udp-which-is-better/).

### Regional VPN Servers
Use the *setRegions()* method to use VPN servers within a country region.
To get all available regions, use the *getAllRegions()* method. 
```python
v = VPN()                           # create VPN object
regions=v.getAllRegions()           # returns a list of all available regions
v.setRegions(["us","de","fr"])      # "us" = USA, "de" = Germany, "fr" = France
v.setRegions("jp")                  # works with only one region. returns False when not available
```
To get a list of available servers within a region, use the *getVPNs()* method.
```python
v = VPN(regions=["uk"])             # only use VPN servers in UK
print(v.getVPNs())                  # will print all servers in UK
print(v.getVPNs(["us","de","fr"]))  # will print all servers in the USA, Germany and France
```

### Log Files
Initially, all log files are stored in the VPNdata subfolder as *vpn_states.csv*.
However, if you do not want to save any logs, change the *make_vpnlist* parameter to *False*.
You can also change the *VPNdata* subfolder and the name of the saved log file *vpn_acc.txt*.
To store your log files and credentials in a different folder, change the folder to *vpn_csvfolder=""* and add your path to the files *vpn_csv="/path/vpn_states.csv "* and *vpn_file="/path/vpn_acc2.txt "*.

```python
v = VPN(make_vpnlist=False,         # create no log file
        vpn_csvfolder="VPNdata2",   # change folder of log file
        vpn_file="vpn_acc2.txt",    # change credential information file in folder VPNdata2
        vpn_csv="vpn_states2.csv")  # change target .csv log file
v.make_vpnlist=True                 # create log file (default=True)
```
The .csv log file contains the list of connected VPN servers, their current status and timestamps of connection attempts as well as previous connection states.

### Verbose output
By default, VPN outputs all information including the connection status on your terminal.
If you want to suppress the information on the terminal, set the *verbose = False* parameter.
```python
v = VPN(verbose=True)   # by default all information is printed on your terminal             
v.verbose=False         # suppress most print output
```

### Get your public IP
To get your current public IP, use *getIP()*.
```python
print(VPN().getIP())    # prints your public IP as string
```

## Startup script
To automatically connect to a VPN server when you start your PC, you can use the additional scripts provided.
### Setup Script
First, check if you have *argparse* for Python installed. Run the [connectVPN.py](https://github.com/M-Schrapel/NordVPN_Connector/blob/main/connectVPN.py) script.
```
$ python /path_to_this_repository/connectVPN.py
```
Your public IP will be changed now. You can check this [here](https://whatismyipaddress.com/).

Now, open your terminal and type:
```
$ sudo nano /etc/rc.local
```
Add the following line to the file with the path to this directory:
```
$ python /path_to_this_repository/connectVPN.py
```
Save the file by pressing <kbd>Ctrl</kbd> + <kbd>o</kbd> and then press <kbd>Enter</kbd>.
After rebooting your PC, you will be automatically connected to a VPN.
### Additional Params
Additionally, you can specify a region for your VPN by passing the *region* argument and a desired country (here *uk*):
```
$ python /path_to_this_repository/connectVPN.py --region uk
```
Congratulations! You can now surf the web anonymously at startup.
To disconnect you can run this simple script:
```
$ python /path_to_this_repository/disconnectVPN.py
```
You can also create executable Bash scripts on your desktop for easy use.


## License
This repository is provided by Maximilian Schrapel under MIT license. For inquiries, feel free to contact me.