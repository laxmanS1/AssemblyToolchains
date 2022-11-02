#!/bin/bash

#Vincent Lo
#Assignment 1 
#Instructor: Lubos Kuzma
#2022-10-31
#purpose: Automated script to install necessary applications and changes to files to run scripts from ITSC204 github. 

sudo apt-get install wget gpg -y
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg
sudo apt install apt-transport-https -y
sudo apt update
sudo apt install code -y
wget -O vscode_extensions.vsix https://marketplace.visualstudio.com/_apis/public/gallery/publishers/rights/vsextensions/nas-vscode/0.0.1/vspackage
code --install-extension vscode_extensions.vsix
rm -rf vscode_extensions.vsix
sudo apt-get install gdb -y
bash -c "$(curl -fsSL https://gef.blah.cat/sh)"
sudo apt install qemu-user -y
sudo apt-get install git -y
sudo apt-get update
sudo apt-get upgrade -y
mkdir /home/kali/Documents/ITSC_204
cd /home/kali/Documents/ITSC_204
sudo git clone https://github.com/LubosKuzma/AssemblyToolchains.git
cd AssemblyToolchains/scripts
sudo chmod +x *
echo "export PATH=\$PATH:$(pwd)" >> ~/.bashrc