from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from jwt import DecodeError

from exceptions.jwt_decode_error import JWTDecodeError
from utils.encryption_utils import EncryptionUtils
# from jwt import (
#     JWT,
#     jwk_from_dict,
#     jwk_from_pem, jwk_from_bytes,
# )

from utils.schema.token import Token
from utils.schema.token_input import TokenInput


class JWTUtils:
    """
    Encode the message to JWT(JWS).
    """

    @staticmethod
    def encode_jwt(data: TokenInput):
        iat = datetime.now(timezone.utc)
        message = Token(iss="music_storage_system",
                        sub=data.user_data.id,
                        iat=iat.timestamp(),
                        user_id=data.user_data.id,
                        permissions=[data.role.role_name],
                        exp=(iat + timedelta(minutes=5)).timestamp()
                        )
        # A RSA key from a PEM file.
        with open(f'{JWTUtils.get_project_root()}/private_key_for_testing_purposes.pem', 'rb') as fh:
            signing_key = fh.read()
        compact_jws = jwt.encode(message.dict(), signing_key, algorithm='EdDSA')
        return compact_jws

    @staticmethod
    def store_jwt_in_config(token: str):
        file = open('music_storage_system_config', "w")
        encrypted_token = EncryptionUtils.encrypt(token)
        file.write(f'token:{encrypted_token}')

    @staticmethod
    def decode_jwt(jwt_token: str) -> Token:
        try:
            with open(f'{JWTUtils.get_project_root()}/public_key_for_testing_purposes.pem', 'rb') as fh:
                verifying_key = fh.read()

            message_received = jwt.decode(
                jwt_token,
                verifying_key,
                algorithms=["EdDSA"]
            )

            token: Token = Token(
                iss=message_received["iss"],
                sub=message_received["sub"],
                iat=message_received["iat"],
                exp=message_received["exp"],
                user_id=message_received["user_id"],
                permissions=message_received["permissions"]
            )
            return token
        except DecodeError:
            raise JWTDecodeError("Cannot decode")

    @staticmethod
    def get_project_root() -> Path:
        return Path(__file__).parent.parent
