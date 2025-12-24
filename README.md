finalpass v2.1.0
================
**The only local password manager and generator, *I* will ever need.** <br>

```
Version: v2.1.0

Author: MrDerpus

Description:
A secure CLI password generator & manager.

Python 3.12.3
Ubuntu Linux 24.04.3 LTS
```
<br>


What changed?
=============
1. I got rid of the need for SQLite to be installed on a users device, and replaced it with a [custom data format called: TOME.](https://github.com/MrDerpus/TOME)

2. Started to use the python library click for console commands, instead of python sys.argvs

3. Started using rich for better error messages and for a better styled output in places.

I originally wanted to make this program as light and as small as possible, by using as little external python libraries as possible.
This was quite silly, so I decided to use external libraries instead of trying to reinvent the wheel.
<br><br>

Why TOME?
=========
I got sick of using SQL for simple projects, the language is perfect - but I think it is over kill for a lot of smaller projects.<br>
This is a much simpler and a more light weight option for this particular project, especially.

TOME is used for program config files, using the MASSADD command & is the database layout that gets encrypted.<br>
The reason why I am using it so much in this project, is because It's just easier to use the TOME parser to parse the data.
<br><br>

# Setup and install as system wide command:
```sh
chmod +x setup-install.sh
./setup.sh
```
<br>

# Commands:
1. add:
```sh
# Add service with all parameters.
finalpass add --service facebook --email fake@email.com --username user-name
finalpass add -s facebook -e fake@email.com -u user-name
```

You must pass at least the service for that entry to be saved, and the password to be generated.<br>
The database is set with a sha512 hash of the users desired password. 
The database password is never stored in the database.

<br><br>
2. massadd
```sh
finalpass massadd massadd-file.tome
```
This allows you to add multiple inputs to the encrypted database with a single password entry, and using a single TOME file.<br>
See massadd TOME file format standards at the bottom of the README.md

<br><br>
3. show:
```sh
finalpass show
```
This will show the list of saved services in the database in a table format.

<br><br>
4. select:
```sh
# Select password associated with service.
# The password is decrypted and sent to the users clipboard for 8 seconds (Default),
# then the clipboard is cleared.
finalpass select facebook password
```

<br><br>
5. remove:
```sh
# Remove entire entry associated with given service name.
finalpass remove facebook
```


<br><br>
6. change:
```sh
# Edit the name of a given service in the database.
finalpass change facebook service new-service-name

# Edit the email associated with given service in database.
finalpass change facebook email new@email.com

# Edit the username in associated with given service in database.
finalpass change facebook username 'John Doe'

# Generate a new password for the associated service in database.
finalpass change facebook password
```


<br><br>
7. version:
```sh
# Display finalpass version, and TOME version.
finalpass version
```

---

# TOME config file
```ini

; Table name with named columns
config[key, value]:
	; vvv  Where the database will be stored.  vvv
	database_location, /home/<username>/.config/finalpassv2
	; vvv  The name of the database you want create/access vvv
	database_name, encrypted_database.db
	; vvv  Time (in seconds) it will take to clear your clipboard after specified time vvv
	clipboard_clear_time, 8
	; vvv  # Length of generated password.  vvv
	password_length, 40
!

```




---
<br>

# Uninstallation:
```sh
# Deletes the config file & database file.
sudo rm -rf ~/.config/finalpassv2

# Deletes the executable.
sudo rm -rf /usr/local/bin/finalpass
```

---
<br>

# massadd CSV file formatting.
```ini
; Database name MUST be the same name as your file name.
massadd[service, email, username]:
	0000, 0000@email.com, username-0000
	0001, 0001@email.com, username-0001
	0002, 0002@email.com, username-0002
	0003, 0003@email.com, username-0003
	0004, 0004@email.com, username-0004
	0005, 0005@email.com, username-0005
!
```

# [Click here to see more about TOME](https://github.com/MrDerpus/TOME)