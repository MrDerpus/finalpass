'''
Version: v1.2.0

Author: MrDerpus

Description:
A secure CLI password generator & manager.

Python 3.12.3
Ubuntu Linux 24.04.3
'''
# finalpass add service=facebook email=email@email.com username=username-here
# ^^^ This will add a service, email, username and then generate, encrypt & add a random password to the DB

# finalpass select password service=facebook
# ^^^ This will copy the unencrypted password associated to a service in a database to the clipboard. 

from sys      import argv, exit as kill
from settings import function as func, AES, database
from os.path  import exists, join

from random   import shuffle
from hashlib  import sha512 as hash
import traceback

from pysqlcipher3 import dbapi2 as sqlite3


# Read config file
config_file = func.read_config_file()
database_location = config_file['database_location']
clear_time = int(config_file['clipboard_clear_time'])
password_length = int(config_file['password_length'])
#print(config_file)

version = '1.2.0'

# Remove main.py from argument list
arguments = argv
if(arguments[0] == 'main.py' or './finalpass' or 'finalpass'):
	arguments.remove(arguments[0])

# Create & setup db if it does not exist.
db_file = join(database_location, 'encrypted_passwords.db')

# Database setup.
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
			cursor.execute(f'PRAGMA kdf_iter = {database.kdf};')
			database.create_db(cursor=cursor)
			connect.commit()
			connect.close()
			del pass_attempt_1, pass_attempt_2, database_password
			break
		else: print('\n\n')


# Connect to Database
connect  = sqlite3.connect(db_file)
cursor   = connect.cursor()


# loop through commands
if(len(arguments) == 0):
	func.Print(' No arguments given.', fg='bright_red')
	kill()

arguments[0] = arguments[0].upper()
function = arguments[0]
arguments.remove(function)
match function:

	# Display version
	case 'VERSION':
		print(f'\n finalpass version: v{version}')


	# Add a service.
	case 'ADD':
		
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
		


		database.add(cursor=cursor, service=service, email=email, username=username, password_length=password_length)
		connect.commit()
		connect.close()


	# Select item from table (service, email, username, password)
	case 'SELECT':

		# Select entry from 
		try:
			flag = arguments[1].split('=')
			flag_name = flag[0].strip()
			value     = flag[1].strip()
			item      = arguments[0].strip()


		except Exception as e:
			func.Print(f' Flag error: \n{e}\n', fg='bright_red')
			kill()

		database.select(cursor=cursor, item=item, flag=flag_name, value=value, sleep_time=clear_time)
		connect.commit()
		connect.close()


	# list services within database.
	case 'LIST':
		database_password = func.passinput(' Enter password: ')
		cursor.execute(f'PRAGMA key = "{database_password}";')
		cursor.execute(f'PRAGMA kdf_iter = {database.kdf};')
		del database_password

		service_list = cursor.execute('SELECT service FROM database;').fetchall()
		connect.commit()
		connect.close()
		
		print('\n------[ Services ]------')
		for i in range(len(service_list)):
			func.Print(f'| {service_list[i][0]}', fg='bright_cyan')
			print('------------------------')


	# Remove entire entry associated with the provided service.
	case 'REMOVE':
		database_password = func.passinput(' Enter password: ')
		cursor.execute(f'PRAGMA key = "{database_password}";')
		cursor.execute(f'PRAGMA kdf_iter = {database.kdf};')
		del database_password

		try:
			flag = arguments[0].split('=')
			flag_name = flag[0].strip()
			value     = flag[1].strip()


		except Exception as e:
			func.Print(f' Flag error: \n{e}\n', fg='bright_red')
			kill()
		

		service = value
		cursor.execute(f'DELETE FROM database WHERE service = "{service}";')
		connect.commit()
		connect.close()
		func.Print(f' Removed {value} from saved passwords.')


	# Change item in database.
	case 'CHANGE':

		try:
			flag = arguments[1].split('=')
			flag_name = flag[0].strip()
			value     = flag[1].strip()
			item = arguments[0]

		except Exception as e:
			func.Print(f'{e}', fg='bright_red')
			traceback.print_exc()
			kill()


		database_password = func.passinput(' Enter password: ')
		cursor.execute(f'PRAGMA key = "{database_password}";')
		cursor.execute(f'PRAGMA kdf_iter = {database.kdf};')

		if(item == 'password'):
			new_password = func.generate()
			encrypted_password = AES.encrypt(database_password, new_password)

			command = 'UPDATE database SET password = ? WHERE service = ?;'
			cursor.execute(command, (encrypted_password, value))
			func.Print(f' Password for {value} successfully changed.', fg='bright_green')

		elif(item in ['service', 'email', 'username']):
			if(len(arguments) < 3): #awww
				func.Print(f' Missing new value. Example: change {item} new_value service=oldservice', fg="bright_red")
				kill()

			new_value = arguments[2].strip()
			old_service = value

			command = f'UPDATE database SET {item} = ? WHERE service = ?;'
			cursor.execute(command, (new_value, old_service))
			func.Print(f' {item.capitalize()} for {old_service} updated to "{new_value}".', fg='bright_green')

		

		del database_password
		connect.commit()
		connect.close()
	

	# return error when given a false function.
	case _:
		func.Print(f' {function} is not a valid function.\n version, add, select, list, remove & change are valid options', fg='bright_red')

kill()
# -----------