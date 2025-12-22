version:str = 'v2.0.0'
'''
Finalpass v2.0.0

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

from pyperclip import copy as pycopy
import click

from settings import function as func
from file_handling import String
from TOME import TOME # TOME v1.3.1

from sys  import exit as kill
from time import sleep
import textwrap
import gc
import os
username:str      = os.getlogin()
directory:str     = os.path.join('./home', username, '.config', 'finalpassv2')
config_path:str   = os.path.join(directory, 'config.tome')
database_path:str = os.path.join(directory, 'db.tome')
delimiter:str = '<9d1796cb-87f5-4c40-98e5-67e7a18b7d8e>' # used only for the database only.


# create settings file and database location if it doesn't exist.
if not os.path.exists(config_path):

	os.makedirs(directory)

	# Write default config settings.
	default_settings = textwrap.dedent(f'''\
	; TOME does not have mixed values by default.
	; Both KEY and VALUE are treated as strings.
	; clipboard_clear_time & password_length have their values converted to integers in the main program. 
	config[key, value]:
		database_location, {directory}
		database_name, db.tome
		clipboard_clear_time, 20
		password_length, 32
	!''')

	with open(config_path, 'w') as file:
		file.write(default_settings)


if not os.path.exists(database_path):
	database = f'passwords[service{delimiter} username{delimiter} email{delimiter} password]:\n'
	
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


# READ config settings
settings:dict = TOME.read(config_path)
database_location:str    = settings['config'][0]['value']
database_name:str        = settings['config'][1]['value']
clipboard_clear_time:int = int(settings['config'][2]['value'])
password_length:int      = int(settings['config'][3]['value'])
database_path:str = os.path.join(database_location, database_name)




@click.group()
def cli(): pass




# Add entry to TOME/Database file.
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
	database = String.decrypt(database_password, enc_database)
	database += f'{service}{delimiter}{username}{delimiter}{email}{delimiter}{func.generate(password_length)}\n'

	enc_database = String.encrypt(database_password, database)

	with open(database_path, 'wb') as file:
		file.write(enc_database)

	del database_password, enc_database, database
	gc.collect()
cli.add_command(add)



@click.command()
def list() -> None:
	database_password = func.passinput(' Enter database password: ')

	# Read from database file
	with open(database_path, 'rb') as file: enc_database = file.read()

	# Decrypt data
	dec_database:str  = String.decrypt(database_password, enc_database)
	database:dict = TOME.read(dec_database, from_string=True, delimiter=delimiter)
	database = database['passwords']

	for i in range(len(database)):
		Print(database[i]['service'])

	del database_password, dec_database, database
	gc.collect()
cli.add_command(list)



# select column value, from user defined service
@click.command()
@click.argument('service')
@click.argument('item')
def select(service:str, item:str) -> None:
	database_password = func.passinput(' Enter database password: ')

	# Read from database file
	with open(database_path, 'rb') as file: enc_database = file.read()

	# Decrypt data
	database:str  = String.decrypt(database_password, enc_database)
	database:dict = TOME.read(database, from_string=True, delimiter=delimiter)
	database = database['passwords']

	match item:
		case 'password':
			for i in range(len(database)):
				if database[i]['service'] == service:
					pycopy(database[i][item])
					sleep(clipboard_clear_time)
					pycopy('')
					break

		case _:
			for j in range(len(database)):
				if database[j]['service'] == service:
					Print(database[i][item])
					break
cli.add_command(select)







if __name__ == '__main__':
	cli()