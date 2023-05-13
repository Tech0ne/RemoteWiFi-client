#!/bin/bash

if [ "$EUID" -ne 0 ]
then
    echo "This is an install process !"
    echo "Please run as root !!!"
    exit 1
fi

if [ -f "/usr/local/bin/remote_wifi" ]
then
    echo "Seems like you already installed this tool."
    echo "If you don't, then what tf is the file /usr/local/remote_wifi ???"
    echo "Remove this file to install RemoteWiFi-Client."
fi

read -p "Please enter your default package manager (apt-get, dnf...) : " pmanager

$pmanager install -y python3 python3-pip sshuttle sshpass

mkdir -p /usr/local/bin/

cp main.py /usr/local/bin/remote_wifi
chmod +x /usr/local/bin/remote_wifi

echo "The file /usr/local/bin/remote_wifi is now available."
echo "Ensure that \"/usr/local/bin\" is in your PATH ($PATH), and you should have a \"remote_wifi\" command available."