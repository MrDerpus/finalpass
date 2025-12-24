#!/bin/bash

# Variable declaration
CURRENT_DIR=$PWD
INSTALL_LOC="/usr/local/bin"
CONFIG_LOC="$HOME/.config/finalpassv2"
CONFIG_FILE="$CONFIG_LOC/config.tome"
DATABASE_NAME="encrypted_database.db"
CLEAR_TIME=8 # time in seconds
PASS_LENGTH=40

# create .config directory & create config file
mkdir -p "$CONFIG_LOC"

echo "; TOME does not have mixed values by default.
; Both KEY and VALUE are treated as strings.
; clipboard_clear_time & password_length have their values converted to integers in the main program. 
config[key, value]:
	database_location, $CONFIG_LOC
	database_name, $DATABASE_NAME
	clipboard_clear_time, $CLEAR_TIME
	password_length, $PASS_LENGTH
!" > $CONFIG_FILE

# Install program reqs.txt
python3 -m venv venv
source venv/bin/activate
pip install -r reqs.txt

# Compile python code to executable
pyinstaller finalpass.spec

# Create system wide command
sudo mv ./dist/finalpass $INSTALL_LOC
sudo chmod +x $INSTALL_LOC/finalpass

deactivate