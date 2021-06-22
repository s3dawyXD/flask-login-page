import time
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class cryptography_API:
    """
    encryption module 

    encrypt data with AES 128 bit and generate signature with SHA 256
    """

    def __init__(self):
        pass

    def get_user_ID(self, username: str, password: str, account_num: str) -> bytes:
        """
        generate user_id from username, password and account number

        @params: username, password, account_number : string
        returns: user_id : bytes
        """
        salt = b"passwordpassword"
        key = str(username) + str(password) + str(account_num)
        key = bytes(key, 'utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(key))
        return key

    def encrypt(self, data: list, key: bytes) -> list:
        """
        encrypt list of string data

        _____input data should be a list of strings_____ 

        @params: data: list of string data, key: bytes
        returns: encrypted_data: list of string 
        """
        f = Fernet(key)
        token = []
        for d in data:
            if type(d) != bytes:
                d = bytes(d, 'utf-8')

            token.append(f.encrypt(d).decode('utf-8'))
        return token

    def decrypt(self, data: list, key: bytes) -> list:
        """
        decrypt list of string data

        _____input data should be a list of strings_____ 

        @params: data: list of string data, key: bytes
        returns: decrypted_data: list of string 
        """
        f = Fernet(key)
        token = []
        for d in data:
            if type(d) != bytes:
                d = bytes(d, 'utf-8')

            token.append(f.decrypt(d).decode('utf-8'))
        return token

    def hash(self, password):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(bytes(password, 'utf-8'))
        return str(digest.finalize())

    def check_password(self, hashed_password, text_password):
        return hashed_password == self.hash(text_password)

if __name__ == '__main__':
    pass
