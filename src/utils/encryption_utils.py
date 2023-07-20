import os
from base64 import b64encode, b64decode

from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Random import get_random_bytes

from exceptions.encryption_error import EncryptionError

BLOCK_IV_SIZE = 16
KEY_SIZE = 32

'''
Block Size for AES-256 is 16 bytes. See <a href=https://www.cryptosys.net/manapi/api_blockciphersizes.html/>

Code Referenced from <a href=https://nitratine.net/blog/post/python-gcm-encryption-tutorial/>
'''

class EncryptionUtils:
    """
    Method which implements the AES-256 encryption algorithm in GCM mode.
    The salt is generated using a pseudo random generator which is then used to create the nonce and tag values.
    """

    @staticmethod
    def encrypt(password):
        key = EncryptionUtils.get_encryption_key()
        salt = get_random_bytes(AES.block_size)

        # Scrypt is considered a good algorithm for generating encryption key from a human key. As you can see it also uses a salt value which you should keep secret.
        private_key = scrypt(key, salt, key_len=32, N=2 ** 17, r=8, p=1)

        # create cipher config
        # using the salt the nonce and the tags for the encryption is never reused
        cipher_config = AES.new(private_key, AES.MODE_GCM)

        if type(password) == bytes:
            # return a dictionary with the encrypted text
            cipher_text, tag = cipher_config.encrypt_and_digest(password)
        else:
            cipher_text, tag = cipher_config.encrypt_and_digest(bytes(password, 'utf-8'))
        # In Format cipher_text:salt:nonce:tag
        return f"{b64encode(cipher_text).decode('utf-8')}:{b64encode(salt).decode('utf-8')}:{b64encode(cipher_config.nonce).decode('utf-8')}:{b64encode(tag).decode('utf-8')}"

    """
    Method which implements the AES-256 decryption algorithm in GCM mode.
    For decryption the nonce value and the tag value generate during encryption is required.
    These values help in achieving authenticated encryption. See Readme for reference. 
    """

    @staticmethod
    def decrypt(encrypted_text):
        key = EncryptionUtils.get_encryption_key()
        # decode the dictionary entries from base64
        if type(encrypted_text) == bytes:
            data_to_str = encrypted_text.decode()
            aes_data = data_to_str.split(":")
        else:
            aes_data = encrypted_text.split(":")

        # In Format cipher_text:salt:nonce:tag
        cipher_text = b64decode(aes_data[0])
        salt = b64decode(aes_data[1])
        nonce = b64decode(aes_data[2])
        # The tag is the result of GCM mode which allows authenticated encryption, therefore no one can crate the tag without the key
        tag = b64decode(aes_data[3])

        try:
            # generate the private key from the key and salt
            # Scrypt is considered a good algorithm for generating encryption key from a human key. As you can see it also uses a salt value which you should keep secret.
            private_key = scrypt(key, salt, key_len=32, N=2 ** 17, r=8, p=1)

            # create the cipher config
            cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

            # decrypt the cipher text
            decrypted = cipher.decrypt_and_verify(cipher_text, tag)

            return decrypted
        except ValueError:
            raise EncryptionError("Error: cannot be decrypted")

    @staticmethod
    def get_encryption_key():
        try:
            key = os.environ.get("encryption_key")
        except Exception:
            raise EncryptionError("Error: Key cannot be found")
            # generate a random salt
        return key
