# [x] add    = add new service,  needs db password, generates, encrypts and stores password.
# [x] list   = list service names, needs db password
# [ ] remove = remove service,  needs db password
# [ ] change = change service name or password, needs db password
# [x] select = select service password, needs db password
#
# password is chosen at random, default is 35 characters long.  Why 35? because it's better than 32.
# stored password = encrypted password, protected with hashed db password
'''
Version: v1.0.0

Author: MrDerpus

Description:
A secure CLI password generator & manager.

Python 3.12.3
Ubuntu Linux 24.04
'''
# passman add service=facebook email=email@email.com username=username-here
# ^^^ This will add a service, email, username and then generate, encrypt & add a random password to the DB

# passman select password service=facebook
# ^^^ This will copy the unencrypted password assoiciated to a service in a database to the clipboard. 

from sys      import argv, exit as kill
from settings import function as func, AES, database
from os.path  import exists

from random   import shuffle
from hashlib  import sha512 as hash

from pysqlcipher3 import dbapi2 as sqlite3


# Remove main.py from argument list
arguments = argv
if(arguments[0] == 'main.py'): arguments.remove(arguments[0])



# Create & setup db if it does not exist.
db_file = 'hashed_passwords.db'
if(not exists(db_file)):
	while(True):
		func.Print(' Enter a password that only YOU will remember.\n This password will be used to access your passwords in the database.\n Your password will be hidden.', fg='bright_cyan')
		pass_attempt_1 = func.passinput(' Enter password: ')
		pass_attempt_2 = func.passinput(' Confirm password: ')

		# Compare password.
		if(pass_attempt_1 == pass_attempt_2):
			database_password = pass_attempt_2
			connect  = sqlite3.connect(db_file)
			cursor   = connect.cursor()


			cursor.execute(f'PRAGMA key = "{database_password}";')
			database.create_db(cursor=cursor)
			connect.commit()
			connect.close()
			del pass_attempt_1, pass_attempt_2, database_password
		else: print('\n\n')
	kill()



# Connect to Database
connect  = sqlite3.connect(db_file)
cursor   = connect.cursor()



# loop through commands
function = arguments[0].lower()
arguments.remove(function)
match function:

	# Add a service, 
	case 'add':
		
		service  = 'NULL'
		email    = 'NULL'
		username = 'NULL'

		for i in range(len(arguments)):
			try:
				flag = arguments[i].split('=')
				flag_name = flag[0].strip()
				value     = flag[1].strip()
			except Exception as e:
				func.Print(f' Flag error: \n{e}\n', fg='bright_red')
			
			match flag_name:
				case 'service':  service = value
				case 'email':    email = value
				case 'username': username = value
				case _:
					func.Print(f' Unknown flag:\n{flag}\n', fg='bright_red')
					kill()
		


		database.add(cursor=cursor, service=service, email=email, username=username)
		connect.commit()
		connect.close()


	# Select item from table (service, email, username, password)
	case 'select':

		try:
			flag = arguments[1].split('=')
			flag_name = flag[0].strip()
			value     = flag[1].strip()
			item      = arguments[0].strip().strip()


		except Exception as e:
			func.Print(f' Flag error: \n{e}\n', fg='bright_red')

		database.select(cursor=cursor, item=item, flag=flag_name, value=value)
		connect.commit()
		connect.close()


	# list services
	case 'list':
		# Create table

		database_password = func.passinput(' Enter password: ')
		cursor.execute(f'PRAGMA key = "{database_password}";')

		command = 'SELECT service FROM database;'
		service_list = cursor.execute('SELECT service FROM database;').fetchall()
		connect.commit()
		connect.close()
		
		print('\n------[ Services ]------')
		for i in range(len(service_list)):
			func.Print(f'| {service_list[i][0]}', fg='bright_cyan')
			print('------------------------')

kill()
# -----------