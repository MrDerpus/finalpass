_version:dict = {'finalpass':'v2.0.1', 'TOME':'v1.4.0'}
'''
Finalpass v2.0.1

Author: MrDerpus

Python 3.12.3
Ubuntu 24.03.3 LTS

Now using TOME v1.3.1, a custom made data language with SQL-like table definition
and CSV data entry. can also support:
Python dict <> TOME <> JSON <> Python dict 


Support Linux for now.
Support CLi application for now.
'''

from rich.traceback import install; install(show_locals = True)
from rich.console   import Console; Print = Console().print
from rich.table     import Table

from pyperclip import copy as pycopy
import click

from settings      import function as func
from file_handling import String
from TOME import TOME # TOME v1.3.1

from sys  import exit as kill
from time import sleep
import textwrap
import gc
import os

import platform

user_platform:str = platform.system().upper()
username:str  = os.getlogin()
directory:str = ''

if user_platform == 'LINUX':
	directory = os.path.join('./home', username, '.config', 'finalpassv2')

#elif user_platform == 'WINDOWS': # NEEDS TESTING
#	directory = os.path.join('C', 'Users', username, '.config', 'finalpassv2')

else:
	print(f' We are sorry, but finalpass is not currently supported for your os:\n {user_platform}\n')
	kill()

config_path:str = os.path.join(directory, 'config.tome')
delimiter:str   = '<9d1796cb-87f5-4c40-98e5-67e7a18b7d8e>' # used only for the encrypted database only.



# READ config settings
settings:dict = TOME.read(config_path)
settings = settings['config']
database_location:str    = settings[0]['value']
database_name:str        = settings[1]['value']
clipboard_clear_time:int = int(settings[2]['value'])
password_length:int      = int(settings[3]['value'])
database_path:str = os.path.join(database_location, database_name)



if not os.path.exists(database_path):
	database = f'passwords[service:str{delimiter} username:str{delimiter} email:str{delimiter} password:str]:\n'
	
	password = ['0', '1']
	while password[0] != password[1]:
		password[0] = func.passinput(' Enter a secure password only YOU will remember: ')
		password[1] = func.passinput(' Confirm your password: ')
		print()
		
	database_password = password[1]


	enc_database = String.encrypt(database_password, database)

	with open(database_path, 'wb') as file:
		file.write(enc_database)

	del password, database_password, database, enc_database
	gc.collect()

	Print(' Your password has been set.')
	kill()







@click.group()
def cli(): pass




# Add entry to TOME Database file.
@click.command()
@click.option('--service',  '-s', default = 'NULL')
@click.option('--username', '-u', default = 'NULL')
@click.option('--email',    '-e', default = 'NULL')
#@click.option('--overwrite','-o', default = False)
def add(service:str, username:str, email:str) -> None:

	if service == 'NULL':
		print(' No service was specified, killing program.')
		kill()

	database_password = func.passinput(' Enter database password: ')

	# Read from database file
	with open(database_path, 'rb') as file:
		enc_database = file.read()

	# Decrypt data
	dec_database = String.decrypt(database_password, enc_database)

	# check to make sure the user is not adding a service with the same name
	database = TOME.read(dec_database, from_string=True, delimiter=delimiter)
	database = database['passwords']	
	func.check_service(service, database)

	dec_database += f'{service}{delimiter}{username}{delimiter}{email}{delimiter}{func.generate(password_length)}\n'

	# encrypt data
	enc_database = String.encrypt(database_password, dec_database)


	# write data
	with open(database_path, 'wb') as file:
		file.write(enc_database)

	del database_password, enc_database, dec_database
	gc.collect()
cli.add_command(add)



@click.command()
@click.argument('input')
def massadd(input:str) -> None:
	input = input.strip()

	if not os.path.exists(input):
		Print(f' "{input}" does not exist.', style='#ff0000')
		kill()

	database_password = func.passinput(' Enter database password: ')

	# Read from database file
	with open(database_path, 'rb') as file:
		enc_database = file.read()

	
	massadd = TOME.read(input)
	massadd = massadd[input.split('.')[0].strip()]

	# Decrypt data
	dec_database = String.decrypt(database_password, enc_database)

	# check to make sure the user is not adding a service with the same name
	database = TOME.read(dec_database, from_string=True, delimiter=delimiter)
	database = database['passwords']	

	for i in range(len(massadd)):
		service:str  = massadd[i]['service']
		email:str    = massadd[i]['email']
		username:str = massadd[i]['username']

		func.check_service(service, database)

		dec_database += f'{service}{delimiter}{username}{delimiter}{email}{delimiter}{func.generate(password_length)}\n'

	# encrypt data
	enc_database = String.encrypt(database_password, dec_database)

	# write data
	with open(database_path, 'wb') as file:
		file.write(enc_database)
cli.add_command(massadd)


@click.command()
def show() -> None:
	database_password = func.passinput(' Enter database password: ')

	# Read from database file
	with open(database_path, 'rb') as file:
		enc_database = file.read()

	# Decrypt data
	dec_database:str = String.decrypt(database_password, enc_database)
	database:dict    = TOME.read(dec_database, from_string=True, delimiter=delimiter)
	database = database['passwords']

	table = Table(title='Services')
	table.add_column('Service',  style='#ff00ff')
	table.add_column('Email',    style='#ffff00')
	table.add_column('Username', style='#00ffff')

	for i in range(len(database)):
		data = database[i]
		table.add_row(data['service'], data['email'], data['username'])
		#data_string = f'| {data["service"]} {data["email"]} {data["username"]}'
		#Print(data_string, style='#00ffff')
	Print(table)
	del database_password, dec_database, database
	gc.collect()
cli.add_command(show)



# select column value, from user defined service
@click.command()
@click.argument('service')
@click.argument('item')
def select(service:str, item:str) -> None:
	database_password = func.passinput(' Enter database password: ')

	# Read from database file
	with open(database_path, 'rb') as file: enc_database = file.read()

	# Decrypt data
	dec_database:str = String.decrypt(database_password, enc_database)
	database:dict    = TOME.read(dec_database, from_string=True, delimiter=delimiter)
	database = database['passwords']

	#print(f'{service=}, {item=}')

	match item:
		case 'password':
			for i in range(len(database)):
				if database[i]['service'] == service:
					pycopy(database[i][item])

					if clipboard_clear_time > 0: 
						sleep(clipboard_clear_time)
						pycopy('')
					break
	'''
	case _:
		column = service
		for j in range(len(database)):
			Print(database[j][item])
			if database[j][str(service)] == service:
				print(database[j][item])
				print('wow')
				break
	'''

	del database_password, database, dec_database
	gc.collect()
cli.add_command(select)



@click.command()
@click.argument('service')
def remove(service:str) -> None:
	database_password = func.passinput(' Enter database password: ')

	# Read from database file
	with open(database_path, 'rb') as file:
		enc_database = file.read()

	# Decrypt data
	dec_database = String.decrypt(database_password, enc_database)

	# check to make sure the user is not adding a service with the same name
	database = TOME.read(dec_database, from_string=True, delimiter=delimiter)	
	#func.check_service(service, database)

	for i in range(len(database['passwords'])):
		remove_item = database['passwords']
		if remove_item[i]['service'] == service:
			database['passwords'].remove(remove_item[i])
			
			string_database = String.encrypt(database_password, TOME.write(to_string=True, table=database, delimiter=delimiter))

			with open(database_path, 'wb') as file:
				file.write(string_database)

			break

			del database_password, remove_item, dec_database, string_database, enc_database, database
			gc.collect()
cli.add_command(remove)



#@click.command()
#@click.argument('service')
#def change(service:str):
#	...

@click.command()
def version(version=_version):
	Print(f'''\
	Finalpass: {version["finalpass"]} https://github.com/MrDerpus/finalpass/tree/v2.0.0
	TOME: {version["TOME"]} https://github.com/MrDerpus/TOME
	''')
cli.add_command(version)

if __name__ == '__main__':
	cli()