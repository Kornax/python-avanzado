from cryptography.fernet import Fernet
key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
cipher_suite = Fernet(key)

password = input("Ingrese Password: ")

ciphered_text = cipher_suite.encrypt(password.encode("utf-8"))   #required to be bytes
print(ciphered_text) 