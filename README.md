finalpass v1.0.0
================

**The last local password manager and generator, *I* will ever need.**

```py
'''
Version: v1.0.0

Author: MrDerpus

Description:
A secure CLI password generator & manager.

Python 3.12.3
Ubuntu Linux 24.04
'''
```

<br>

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

# Commands:
## 1. add:
```sh
python3 main.py add service=facebook email=fake@email.com username=user-name
```
### The password as auto generated and encrypted with AES256.
---

