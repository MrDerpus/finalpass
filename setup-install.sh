#!/bin/bash


# Variable declaration
CURRENT_DIR=$PWD
INSTALL_LOC="/usr/local/bin"
CONFIG_LOC="$HOME/.config/finalpass"
CONFIG_FILE="$CONFIG_LOC/finalpass.conf"
DATABASE_NAME="encrypted_database.db"

# create .config directory & create config file
mkdir -p "$CONFIG_LOC"
echo "database_location=$CONFIG_LOC" >> "$CONFIG_FILE"
echo "database_name=$DATABASE_NAME"  >> "$CONFIG_FILE"
echo "clipboard_clear_time=15"       >> "$CONFIG_FILE"
echo "password_length=32"            >> "$CONFIG_FILE"

# Install dependencies for pysqlchipher3
sudo apt update
sudo apt install -y python3.12-dev libsqlcipher-dev zlib1g-dev build-essential xclip
sudo apt install --reinstall zlib1g=1:1.3.dfsg-3.1ubuntu2 zlib1g-dev

# Install program reqs.txt
python3 -m venv venv
source venv/bin/activate
pip install -r reqs.txt

# Compile python code to executable
pyinstaller finalpass.spec

# Create system wide command
sudo mv $CURRENT_DIR/dist/finalpass $INSTALL_LOC/finalpass
sudo chmod +x $INSTALL_LOC/finalpass

deactivate
