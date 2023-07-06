import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)
from jwt.utils import get_int_from_datetime

from utils.schema.Token import Token


class JWTUtils:
    instance = JWT()

    """
    Encode the message to JWT(JWS).
    """
    @staticmethod
    def encode_jwt(sub: str = ""):
        iat = datetime.now(timezone.utc)
        message = Token(iss="music_storage_system",
                        sub=sub, iat=get_int_from_datetime(iat),
                        exp=get_int_from_datetime(
                            iat + timedelta(minutes=5)))
        # A RSA key from a PEM file.
        with open(f'{JWTUtils.get_project_root()}/private_key_for_testing_purposes.pem', 'rb') as fh:
            signing_key = jwk_from_pem(pem_content=fh.read())
        compact_jws = JWTUtils.instance.encode(message.dict(), signing_key, alg='RS256')
        return compact_jws

    @staticmethod
    def store_jwt_in_config(token: str):
        file = open(f'music_storage_system_config', "w")
        file.write(f'token:{token}')

    @staticmethod
    def decode_jwt(jwt_token: str):
        with open(f'{JWTUtils.get_project_root()}/public_key.json', 'r') as fh:
            verifying_key = jwk_from_dict(json.load(fh))

        message_received = JWTUtils.instance.decode(
            jwt_token, verifying_key, do_time_check=True)
        return message_received

    @staticmethod
    def get_project_root() -> Path:
        return Path(__file__).parent.parent
