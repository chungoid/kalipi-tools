# kalipi-tools
 general kalipi config/usage

 this script makes headless setup quick. flash your sd card with a fresh install and drag an empty file named "ssh" into your boot partition. Drag a file named "wpa_supplicant.conf" into your boot folder and use the template below for wpa_supplicant.conf

 ctrl_interface=DIR/var/run/wpa_supplicant GROUP=netdev
 update_config=1
 country=US
 network={
    ssid="yourNetworkName"
    psk="yourNetworkPassword"
 }

#How to use
git clone https://github.com/chungoid/kalipi-tools
cd kalipi-tools
python setup.py

enjoy

