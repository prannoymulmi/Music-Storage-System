import hashlib
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

from exceptions.encryption_error import EncryptionError

BLOCK_IV_SIZE = 16
KEY_SIZE = 32

'''
Block Size and Initialization Vector (IV) for AES-256 is 16 bytes. See <a href=https://www.cryptosys.net/manapi/api_blockciphersizes.html/>

Code Referenced from <a href=https://nitratine.net/blog/post/python-gcm-encryption-tutorial/>
'''


def encrypt(password, key: bytes):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)

    # Scrypt is considered a good algorithm for generating encryption key from a human password. As you can see it also uses a salt value which you should keep secret.
    private_key = scrypt(key, salt, key_len=32, N=2 ** 17, r=8, p=1)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(password, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }


def decrypt(enc_dict, password):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])

    try:
        # generate the private key from the password and salt
        # Scrypt is considered a good algorithm for generating encryption key from a human password. As you can see it also uses a salt value which you should keep secret.
        private_key = scrypt(password, salt, key_len=32, N=2 ** 17, r=8, p=1)

        # create the cipher config
        cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

        # decrypt the cipher text
        decrypted = cipher.decrypt_and_verify(cipher_text, tag)

        return decrypted
    except ValueError:
        raise EncryptionError("Error: cannot be decrypted")
