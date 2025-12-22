from cryptography.hazmat.primitives.ciphers    import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends   import default_backend
from cryptography.hazmat.primitives import hashes
import os

class String:
	# --- Key derivation from password ---
	@staticmethod
	def derive_key(password:str, salt:bytes) -> bytes:

		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,  # AES-256
			salt=salt,
			iterations=550_000,
			backend=default_backend(),
		)

		return kdf.derive(password.encode('utf-8'))




	# --- Encrypt file ---
	@staticmethod
	def encrypt(password:str, text:str) -> bytes:

		salt:bytes = os.urandom(16)	 # Public
		iv:bytes   = os.urandom(12)	 # Public (AES-GCM nonce)
		key:bytes  = File.derive_key(password, salt)

		encryptor = Cipher(
			algorithms.AES(key),
			modes.GCM(iv),
			backend=default_backend(),
		).encryptor()

		ciphertext = encryptor.update(text.encode()) + encryptor.finalize()
		tag = encryptor.tag  # 16 bytes

		# Store everything needed for decryption in a single binary blob:
		# [ salt | iv | tag | ciphertext ]		
		lst:list = [salt, iv, tag, ciphertext]
		encrypted_data = b''
		for i in range(len(lst)):
			encrypted_data += lst[i]

		return encrypted_data




	# --- Decrypt file ---
	@staticmethod
	def decrypt(password:str, text:bytes) -> str:
		# Layout:
		# salt (16) | iv (12) | tag (16) | ciphertext (rest)
		salt:bytes = text[0:16]
		iv:bytes   = text[16:28]
		tag:bytes  = text[28:44]
		ciphertext:bytes = text[44:]

		key = File.derive_key(password, salt)

		decryptor = Cipher(
			algorithms.AES(key),
			modes.GCM(iv, tag),
			backend=default_backend(),
		).decryptor()

		plaintext = decryptor.update(ciphertext) + decryptor.finalize()

		return plaintext.decode()



class File:

	# --- Key derivation from password ---
	@staticmethod
	def derive_key(password:str, salt:bytes) -> bytes:
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,           # AES-256
			salt=salt,
			iterations=1_000_000,   # Solid modern work factor
			backend=default_backend(),
		)
		return kdf.derive(password.encode('utf-8'))




	# --- Encrypt file ---
	@staticmethod
	def encrypt(password:str, infile:str):

		outfile:str = infile

		salt = os.urandom(16)	 # Public
		iv   = os.urandom(12)	 # Public (AES-GCM nonce)

		key = File.derive_key(password, salt)

		encryptor = Cipher(
			algorithms.AES(key),
			modes.GCM(iv),
			backend=default_backend(),
		).encryptor()

		with open(infile, 'rb') as f:
			plaintext = f.read()

		ciphertext = encryptor.update(plaintext) + encryptor.finalize()
		tag = encryptor.tag  # 16 bytes

		# Store everything needed for decryption in a single binary blob:
		# [ salt | iv | tag | ciphertext ]
		with open(outfile, 'wb') as f:
			f.write(salt)
			f.write(iv)
			f.write(tag)
			f.write(ciphertext)

		print(f'Encrypted -> {outfile}')




	# --- Decrypt file ---
	@staticmethod
	def decrypt(password:str, infile:str):

		outfile:str = infile

		with open(infile, 'rb') as f:
			data = f.read()

		# Layout:
		# salt (16) | iv (12) | tag (16) | ciphertext (rest)
		salt = data[0:16]
		iv   = data[16:28]
		tag  = data[28:44]
		ciphertext = data[44:]

		key = File.derive_key(password, salt)

		decryptor = Cipher(
			algorithms.AES(key),
			modes.GCM(iv, tag),
			backend=default_backend(),
		).decryptor()

		plaintext = decryptor.update(ciphertext) + decryptor.finalize()

		with open(outfile, 'wb') as f:
			f.write(plaintext)

		print(f'Decrypted -> {outfile}')