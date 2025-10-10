from random    import randint, shuffle
from platform  import system
from getpass   import getpass
from time      import sleep
from sys       import exit as kill
import subprocess
import hashlib
import string
import hmac
import os

from pyperclip import copy as pycopy

from colours   import COLOUR


alphabet = string.punctuation + string.ascii_letters + string.digits
col = COLOUR.Colours



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
				if(not line or line.startswith(('#', ';'))): continue
				
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
	def Print(text:str='', bg:str='black', fg:str='bright_white') -> None:
		bg      = f'bg_{bg}'
		colours = f'{col[bg]}{col[fg]}'
		text    = f'{colours}{text}{col["reset"]}'

		print(text)


	@staticmethod
	def generate(pass_length:int) -> bytes:

		# string to list
		to_list = []
		for i in range(len(alphabet)):
			to_list += [alphabet[i]]

		for j in range(10):
			shuffle(to_list)

		password = ''
		for k in range(pass_length):
			password += to_list[randint(0,len(alphabet)-1)]

		return password.encode()


	@staticmethod
	# Grab user input, and turn it into a sha15 hash
	def passinput(text:str='') -> str:
		hashed_password = hashlib.sha512(getpass(text).encode()).hexdigest()

		return hashed_password



class AES:
	SALT_LEN = 16
	IV_LEN = 16
	KEY_LEN = 32
	DERIVED_LEN = 64
	PBKDF2_ITERS = 200_000

	@staticmethod
	def _derive_keys(password: bytes, salt: bytes):
		'''PBKDF2-HMAC-SHA256 -> encryption key + hmac key'''
		dk = hashlib.pbkdf2_hmac('sha256', password, salt, AES.PBKDF2_ITERS, dklen=AES.DERIVED_LEN)
		return dk[:AES.KEY_LEN], dk[AES.KEY_LEN:]


	@staticmethod
	def _tohex(b: bytes) -> str:
		return b.hex()


	@staticmethod
	def encrypt(password:str, plaintext:bytes) -> bytes:
		password_b = password.encode('utf-8')
		salt = os.urandom(AES.SALT_LEN)
		iv   = os.urandom(AES.IV_LEN)
		key, hmac_key = AES._derive_keys(password_b, salt)

		p = subprocess.run(
			["openssl", "enc", "-aes-256-cbc", "-K", AES._tohex(key), "-iv", AES._tohex(iv), "-nosalt"],
			input=plaintext,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			check=False
		)
		if(p.returncode != 0):
			raise RuntimeError("openssl failed: " + p.stderr.decode('utf-8', errors='replace'))

		ciphertext = p.stdout
		mac = hmac.new(hmac_key, salt + iv + ciphertext, hashlib.sha256).digest()
		
		total = salt + iv + ciphertext + mac
		return total


	@staticmethod
	def decrypt(password:str, package:bytes) -> str:

		package = package


		if(len(package) < AES.SALT_LEN + AES.IV_LEN + hashlib.sha256().digest_size):
			raise ValueError("package too short")

		salt = package[:AES.SALT_LEN]
		iv = package[AES.SALT_LEN:AES.SALT_LEN+AES.IV_LEN]
		mac = package[-hashlib.sha256().digest_size:]
		ciphertext = package[AES.SALT_LEN+AES.IV_LEN:-hashlib.sha256().digest_size]

		password_b = password.encode('utf-8')
		key, hmac_key = AES._derive_keys(password_b, salt)

		# verify HMAC
		expected = hmac.new(hmac_key, salt + iv + ciphertext, hashlib.sha256).digest()
		if not hmac.compare_digest(mac, expected):
			raise ValueError("authentication failed (MAC mismatch)")

		p = subprocess.run(
			["openssl", "enc", "-d", "-aes-256-cbc", "-K", AES._tohex(key), "-iv", AES._tohex(iv), "-nosalt"],
			input=ciphertext,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			check=False
		)
		if(p.returncode != 0):
			raise RuntimeError("openssl decryption failed: " + p.stderr.decode('utf-8', errors='replace'))

	
		return p.stdout.decode()

		# enc password
		# pkg = AES.encrypt('key-2-enc', b'db-password')



class database:
	kdf:int = 640000

	@staticmethod
	def create_db(cursor) -> None:

		# Create table
		command = '''
		CREATE TABLE IF NOT EXISTS database (
			service TEXT PRIMARY KEY,
			username TEXT,
			email TEXT,
			password BLOB
		);
		'''
		cursor.execute(command.strip())		


	@staticmethod
	def add(cursor, password_length, service:str='NULL', email:str='NULL', username:str='NULL') -> None:
		database_password = function.passinput(' Enter database password: ')
		cursor.execute(f'PRAGMA key = "{database_password}";')
		cursor.execute(f'PRAGMA kdf_iter = {database.kdf};')
		
		generated_password = AES.encrypt(database_password, function.generate(password_length))

		command = f'''
		INSERT INTO database (service, username, email, password)
		VALUES(?, ?, ?, ?)
		'''

		cursor.execute(command.strip(), (service, username, email, generated_password))
		del database_password, generated_password


	@staticmethod
	def select(cursor, sleep_time, item:str='NULL', flag:str='NULL', value:str='NULL') -> None:
		
		accepted_keyword = ['service', 'email', 'username', 'password']

		if(flag not in accepted_keyword):
			function.Print(f' {flag} is not a valid keyword, valid keywords are:\n {accepted_keyword}', fg='bright_red')
			kill()
		
		database_password = function.passinput(' Enter database password: ')
		cursor.execute(f'PRAGMA key = "{database_password}";')
		cursor.execute(f'PRAGMA kdf_iter = {database.kdf};')
		
	
		try:
			command = f'SELECT {item} FROM database WHERE {flag} = "{value}";'
			copied_item = cursor.execute(command.strip()).fetchall()[0][0].strip()
		except Exception as e:
			function.Print(f' {flag}={value} could not be found in database.\n', fg='bright_red')
			kill()

		pycopy(copied_item)
		
		# sleep for 10 seconds, allowing time to paste password into password field before deleting clearing.
		skip = False
		if((item == accepted_keyword[3] and skip == False)):
			copied_item = AES.decrypt(database_password, copied_item)
			del database_password
			pycopy(copied_item)
			sleep(sleep_time)
			pycopy('')