import secrets

import pytest

from exceptions.encryption_error import EncryptionError
from utils.encryption_utils import encrypt, decrypt


def test_encryption_and_decryption_when_correct_key_and_encrypted_item_is_a_text_then_is_encrypted_and_decrypted_successfully():
    random_byte_string_key = b"\x00" + secrets.token_bytes(4) + b"\x00"
    plain_text = "test_this_text hello"
    data = encrypt(plain_text, random_byte_string_key)
    result = decrypt(data, random_byte_string_key)
    assert plain_text == result.decode("utf-8")


def test_encryption_and_decryption_when_wrong_key_and_encrypted_item_is_a_text_then_is_encrypted_and_decrypted_successfully():
    random_byte_string_key = b"\x00" + secrets.token_bytes(4) + b"\x00"
    wrong_random_byte_string_key = b"\x00" + secrets.token_bytes(4) + b"\x00"
    plain_text = "test_this_text hello"
    data = encrypt(plain_text, random_byte_string_key)
    with pytest.raises(EncryptionError, match="Error: cannot be decrypted"):
        decrypt(data, wrong_random_byte_string_key)
