finalpass v1.3.0
================

**The only local password manager and generator, *I* will ever need.** <br>

```
Version: v1.3.0

Author: MrDerpus

Description:
A secure CLI password generator & manager.

Python 3.12.3
Ubuntu Linux 24.04.3
```
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
finalpass add service=facebook email=fake@email.com username=user-name
```

You must pass at least one argument for that entry to be saved, and the password to be generated.<br> 
The password is auto generated and encrypted with ***AES256*** before it is stored in the database.<br><br>
The database is also set with a sha512 hash of the users desired password. 
The database password is never stored in the database.

<br><br>
2. massadd
```sh
finalpass massadd massadd-file.csv
```

This allows you to add multiple inputs to the encrypted database with a single password entry, and using a single CSV file.<br>
See massadd CSV file format standards at the bottom of the README.md

<br><br>
3. List:
```sh
finalpass list
```

This will list saved services in the database.

<br><br>
4. select:
```sh
# Select password associated with service.
# The password is decrypted and sent to the users clipboard for 10 seconds,
# then the clipboard is cleared.
finalpass select password service=facebook

# Select email associated with service.
finalpass select email service=facebook

# Select username associated with service.
finalpass select username service=facebook
```

<br><br>
5. remove:
```sh
# Remove entire entry associated with given service name.
finalpass remove service=facebook
```

<br><br>
6. change:
```sh
# Change any item in database table associated with given parameters.
# Change service name.
finalpass change service service=facebook twitter

# Change email address for defined service.
finalpass change email service=twitter new_email@email.com

# Change username for defined service
finalpass change username service=twitter new_username

# Auto generate and encrypt a new password for service. 
finalpass change password service=twitter
```


<br><br>
7. version:
```sh
# Display finalpass version
finalpass version
```

---

# config file
```ini
; Where the database will be stored.
database_location=~/.config/finalpass

# The name of the database you want create/access
database_name=encrypted_database.db

# Time (in seconds) it will take to clear you clipboard after selection password.
clipboard_clear_time=15

# Length of generated password.
password_length=40
```

---
<br>

# Uninstallation:
```sh
# Deletes the config file & database file.
sudo rm -rf ~/.config/finalpass

# Deletes the executable.
sudo rm -rf /usr/local/bin/finalpass
```

---
<br>

# massadd CSV file formatting.
```csv
; service, email, username
# -------------------------

Netflix, fake-user1@email.com, username1
GitHub,  NULL, username2
Twitter, fake-user3@email.com, NULL
Gmail,,
;Ebay,    fake-user4@email.com, username4
```

Comments can be either: **';'** or **'#'** at the start of a line. <br>
Blank lines and comment lines will be ignored. <br>
Lines with with less than 3 comma separated values will also be ignored. <br>
Any entry you do not wish to either enter an email or a username must be equal to ***'NULL'.*** <br>
However, this is also done for you if there is an empty value after a comma.