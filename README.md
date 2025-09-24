finalpass v1.1.0
================

**The only local password manager and generator, *I* will ever need.** <br>

```
Version: v1.1.0

Author: MrDerpus

Description:
A secure CLI password generator & manager.

Python 3.12.3
Ubuntu Linux 24.04.3
```
<br><br>

# Setup and install:
```sh
sudo apt update
sudo apt full-upgrade -y
sudo apt install python3.12-dev libsqlcipher-dev zlib1g-dev build-essential
sudo apt install --reinstall zlib1g=1:1.3.dfsg-3.1ubuntu2 zlib1g-dev

python -m venv venv
source venv/bin/activate
pip install -r reqs.txt
```
<br>

# Commands:
1. add:
```sh
# Add service with all parameters.
python3 main.py add service=facebook email=fake@email.com username=user-name
```
You must pass at least one argument for that entry to be saved, and the password to be generated.<br> 
The password is auto generated and encrypted with ***AES256*** before it is stored in the database.<br><br>
The database is also set with a sha512 hash of the users desired password. 
The database password is never stored in the database.

<br><br>
2. List:
```sh
python3 main.py list
```
This will list saved services in the database.

<br><br>
3. select:
```sh
# Select password associated with service.
# The password is decrypted and sent to the users clipboard for 10 seconds,
# then the clipboard is cleared.
python3 main.py select password service=facebook

# Select email associated with service.
python3 main.py select email service=facebook

# Select username associated with service.
python3 main.py select username service=facebook
```

<br><br>
4. remove:
```sh
# Remove entire entry associated with given service name.
python3 main.py remove service=facebook
```

<br><br>
5. change:
```sh
# Change any item in database table associated with given parameters.
# Change service name.
python3 main.py change service service=facebook twitter

# Change email address for defined service.
python3 main.py change email service=twitter new_email@email.com

# Change username for defined service
python3 main.py change username service=twitter new_username

# Auto generate and encrpyt a new password for service. 
python3 main.py change password service=twitter
```

---