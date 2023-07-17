from datetime import timezone, timedelta, datetime
from unittest import mock
from unittest.mock import ANY

import jwt
import pytest
from freezegun import freeze_time

from exceptions.jwt_decode_error import JWTDecodeError
# from exceptions.jwt_decode_error import JWTDecodeError
# from jwt.utils import get_int_from_datetime

from models.role import Role
from models.user import User
from utils.jwt_utils import JWTUtils
from utils.schema.token import Token
from utils.schema.token_input import TokenInput

"""
Using freeze time to mock date and time, 
so that the test always returns deterministic results
"""
@freeze_time("2023-06-8")
@mock.patch.object(jwt, "encode")
def test_encode_jwt_when_default_sub_then_encode_is_called_with_right_parameters(mock_jwt):
    iat = datetime.now(timezone.utc)
    expected_message = Token(iss="music_storage_system",
                             sub="1",
                             permissions=["test"],
                             user_id="1",
                             iat=iat.timestamp(),
                             exp=(iat + timedelta(minutes=5)).timestamp()
                             )

    JWTUtils.encode_jwt(TokenInput(user_data=User(id=1),
                                   role=Role(
                                       id=1,
                                       role_name="test"
                                   )
                                   ))
    mock_jwt.assert_called_with(expected_message.dict(), ANY, algorithm='EdDSA')

# def test():
#     private_key = Ed25519PrivateKey.generate()
#     private_key_bytes = private_key.private_bytes(encoding=Encoding.PEM, format=PrivateFormat.PKCS8,
#                                     encryption_algorithm=NoEncryption())
#     public_key_bytes = private_key.public_key().public_bytes(encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo)
#     print(private_key_bytes)
#     print(public_key_bytes)
#     res = JWTUtils.encode_jwt(TokenInput(user_data=User(id=1),
#                                    role=Role(
#                                        id=1,
#                                        role_name="test"
#                                    )
#                                    ))
#     res_dec = JWTUtils.decode_jwt(res)
#     print(res_dec)


def test_decode_jwt_when_correct_valid_token_then_returns_decoded_token():
    expected_token = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJtdXNpY19zdG9yYWdlX3N5c3RlbSIsInN1YiI6IjEiLCJpYXQiOjE2ODk0MjMwMDcsImV4cCI6NDg0MzAyMzAwNywidXNlcl9pZCI6IjEiLCJwZXJtaXNzaW9ucyI6WyJ0ZXN0Il19.2XNOlPdNAiMwY6cR8qDO3jDLmkecVsWAStdXO0syZPRrZVPgF-cEGq5fI6CWfHySnc-EltiJ5WRWwf_yE6CpCA"
    res: Token = JWTUtils.decode_jwt(expected_token)
    assert res is not None
    assert res.iss == "music_storage_system"

def test_decode_jwt_when_spoofed_jwt_token_then_token_cannot_be_decoded_error_is_returned():
    spoofed_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiAiYXNtaXMiLCAic3ViIjogIiIsICJpYXQiOiAxNjY4Nzk1MjA0LCAiZXhwIjogMTY2ODc5NzAwNH0.Ps3vactKYLdTswW7zd-8msBofiICxmQHegId>IqNcmaw8DshmCN7TWrARJ8LKmx59jRO3g-MXTqwTYWJSOdMfJD13kV_uciv4ZBmHLzqq-e28Dup4RBQz9uc19rWhilK5fXbP5lpWF4IHukl_9_krDXfYADZPn9zXebxb6QRijkVPLLNnx4Vh_xIo_Yuahsz6X5cINmGrluIkE9G_csRSSPjbSNWwYzi4EE2Dqgi0iEKgkgnPyXCpgJb0YhKHbzmNFsniRZv3HhAZDRFlBiyG2pK0fpaHvD4ZAXu1PZU2RlCbTM4BamMiuNuQE2LqV4DwQU2V9pYFTL7avQ6Pyxp222P1HxZLw8hZe-yOndd60F5aXYY0bGa0GrhZivq1sfI4oUJcV6rtuCaj7HFOLGfGIgOrpMtoOu_P7gxKrOdLuHyUpE8XqeZScildJ5b_58_2lGrIFzeuA8yYlStWNJRr1hbg-PT3x9EEHEF4YboghG-izc07aSpGcn-c1cQQRzjdMEiAwHYX5uZ31b6EwSrRlptl-2gENb04pqE0ea58sHZFjKfKyAyNNfj1etyADWK0w4ziYT_HUuD2X6Kht4dRYV19xWCCKZ1frgsmsZOcZEeBdBMItOfaIPdaFGvGe6mdvRwdmSdFhtDeZuQpxlCLt6rDF6kmGC8Yu5_QmJ3wgK4"
    with pytest.raises(JWTDecodeError):
        JWTUtils.decode_jwt(spoofed_token)
