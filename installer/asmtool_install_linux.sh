#!/bin/bash

# *** Beta version of assmembly toolchain installer (Linux-version) ***

# Created by Geoffrey Yung
# Project host/Instructor: Lubos Kuzma
# ISS Program, SADT, SAIT
# October 2022


# Notification and prompt for user permission
echo "***sudo permission is required for the follwing operations***"
echo "Download scripts from Github with git"
echo "File operations to /opt directoty"
echo "Allow execute rights to script files"
echo "Modification of bash Path element for tool utillization"
echo ""
while true; do
    read -p "Do you wish to proceed with installation?[y/n] " yn
    case $yn in
        [Yy]* ) echo "Starting installation..."; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer with y or n";;
    esac
done

echo "Please provide sudo permission for the process"
sudo git -C /opt clone https://github.com/LubosKuzma/AssemblyToolchains.git 
# get file with git clone to /opt
# /opt is for add-on application software
echo "Download complete..."

# modify scripts execute right with chmod
sudo chmod +x /opt/AssemblyToolchains/scripts/arm_toolchain.sh
sudo chmod +x /opt/AssemblyToolchains/scripts/x86_toolchain.sh
echo "Execute rights modified..."

# add toolchain paths to $PATH 
sudo echo 'export PATH=$PATH:/opt/AssemblyToolchains/scripts' >> ~/.bashrc
echo "Bash PATH element set..."

echo ""
echo "Installation complete"
echo "Type arm_toolchain.sh or x86_toolchain to verify result"
echo "Tips: enter bash to refresh bash PATH element or refresh terminal if toolchain is not executing"

