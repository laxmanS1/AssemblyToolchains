#!/bin/bash

#Created by Renvel Eldridge Dela Cruz
#ISS Program SAIT
#October 2022

echo "Installing updates..."
sudo apt-get update
echo "Update complete"

echo "Installing Virtual Studio Code"
cd Downloads
wget -O vscode_linux.deb https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64
sudo apt-get install ./vscode_linux.deb
rm -rf vscode_linux.deb
echo "Vistual Studio Code installed successfully!"

echo "Installing NASM extension for Visual Studio Code"
wget -O vscode_extensions.vsix https://marketplace.visualstudio.com/_apis/public/gallery/publishers/rights/vsextensions/nas-vscode/0.0.1/vspackage
code --install-extension vscode_extensions.vsix
rm -rf vscode_extensions.vsix
cd ~
echo "NASM extension installed successfully!"

echo "Installing GDB, GEF and Qemu"
sudo apt-get install gdb && bash -c "$(curl -fsSL https://gef.blah.cat/sh)"
sudo apt install qemu-user -y
echo "GDB, GEF and Qemu installed successfully"

echo "Creating and downloading toolchain scripts..."
cd Documents
mkdir AssemblyScripts
cd AssemblyScripts
git clone https://github.com/LubosKuzma/AssemblyToolchains.git
cd scripts
sudo chmod +x *
echo "export PATH=\$PATH:$(pwd)" >> ~/.bashrc
cd ~
echo "Toolchain scripts downloaded successfully!"

echo "You can now use the assembly toolchain on your Visual Studio Code machine!
Just remember to use the bash terminal to run the toolchain script"
