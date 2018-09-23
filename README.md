# Speedtest for multiple network

#Speedtest
#Install speedtest-cli
pip install speedtest-cli

#Crontab
#Edit your crontab with: 
crontab -e
#Insert a new line line like to run every 5 minutes
MAILTO=""
SHELL=/bin/bash
*/5 * * * * /home/username/speedtest.sh > /dev/null 2>$1

#Graph-Builder
#Install dependencies (Ubuntu): 
pip install matplotlib
#Run it: 
python graph-builder.py log-188.146.239.242.csv


#General information
nmcli radio

#To see list of saved connections
nmcli connection

#Skan for wifi
nmcli device wifi rescan

#To see list of available WiFi hotspots
nmcli device wifi list

#Create new connection
nmcli -ask device wifi connect SSID-Name password wireless-password

#Connect to saved network
nmcli connection up SSID-Name

#Chack internet connection
if [[ "$(ping -c 1 8.8.8.8 | grep '100% packet loss' )" != "" ]]; then
    echo "Internet isn't present"
    exit 1
else
    echo "Internet is present"
    wget www.site.com
fi
#or
nm-online [-q]

pip install -U scipy
pip install -U scikit-learn
