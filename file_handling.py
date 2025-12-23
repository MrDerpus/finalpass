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
		key:bytes  = String.derive_key(password, salt)

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

		key = String.derive_key(password, salt)

		decryptor = Cipher(
			algorithms.AES(key),
			modes.GCM(iv, tag),
			backend=default_backend(),
		).decryptor()

		plaintext = decryptor.update(ciphertext) + decryptor.finalize()

		return plaintext.decode()