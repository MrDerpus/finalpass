from rich.console import Console; Print = Console().print

from sys     import exit as kill
from random  import randint, shuffle
from getpass import getpass
import hashlib
import string
import os


alphabet = string.punctuation + string.ascii_letters + string.digits


class function:
	
	@staticmethod
	def read_config_file():
		config_path = os.path.expanduser('~/.config/finalpass/finalpass.conf')
		with open(config_path, 'r') as config:
		#with open('finalpass.conf', 'r') as config:

			return_values = {}

			for line in config:
				line = line.strip()
				# Skip over line if blank or comment.
				if not line or line.startswith(('#', ';')) : continue
				
				line = line.split('=')
				# Skip line if incomplete.
				if(len(line) < 2): continue

				
				# Assign variables.
				variable = line[0].strip()
				value    = line[1].strip()

				match variable:
					case 'database_location':
						return_values[variable] = os.path.expanduser(value)

					case _: return_values[variable] = value
		
		return return_values



	@staticmethod
	def generate(pass_length:int) -> str:

		# string to list
		to_list = []
		for i in range(len(alphabet)):
			to_list += [alphabet[i]]

		# shuffle the list 10 times.
		for j in range(10):
			shuffle(to_list)

		password = ''
		for k in range(pass_length):
			password += to_list[randint(0,len(alphabet)-1)]

		return password


	@staticmethod
	# Grab user input, and turn it into a sha15 hash
	def passinput(text:str) -> str:
		hashed_password = hashlib.sha512(getpass(text).encode()).hexdigest()

		return hashed_password



	@staticmethod
	def check_service(service:str, database:dict, exit:bool=True) -> None:
		
		for i in range(len(database)):
			if database[i]['service'] == service:
				Print(f' Service: "{service}" already exists within your database.', style='#ff0000')
				
				if exit == True: kill()
