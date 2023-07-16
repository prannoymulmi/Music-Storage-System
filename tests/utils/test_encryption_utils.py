import os
import secrets
from unittest import mock

import pytest

from exceptions.encryption_error import EncryptionError
from utils.encryption_utils import EncryptionUtils


@mock.patch.object(os.environ, "get")
def test_encryption_and_decryption_when_correct_key_and_encrypted_item_is_a_text_then_is_encrypted_and_decrypted_successfully(mock_os):
    random_byte_string_key = b"\x00" + secrets.token_bytes(4) + b"\x00"
    mock_os.return_value = random_byte_string_key

    plain_text = "test_this_text hello"
    data = EncryptionUtils.encrypt(plain_text)
    result = EncryptionUtils.decrypt(data)
    assert plain_text == result.decode("utf-8")


@mock.patch.object(os.environ, "get")
def test_encryption_and_decryption_when_wrong_key_and_encrypted_item_is_a_text_then_is_encrypted_and_decrypted_successfully(
        mock_os
):

    random_byte_string_key = b"\x00" + secrets.token_bytes(4) + b"\x00"
    mock_os.return_value = random_byte_string_key

    plain_text = "test_this_text hello"
    data = EncryptionUtils.encrypt(plain_text)
    with pytest.raises(EncryptionError, match="Error: cannot be decrypted"):
        wrong_random_byte_string_key = b"\x00" + secrets.token_bytes(4) + b"\x00"
        mock_os.return_value = wrong_random_byte_string_key
        EncryptionUtils.decrypt(data)
