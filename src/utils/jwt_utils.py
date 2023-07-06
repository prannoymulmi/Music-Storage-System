import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)
from jwt.utils import get_int_from_datetime

from utils.schema.TokenMessage import TokenMessage

instance = JWT()

"""
Encode the message to JWT(JWS).
"""
def encode_jwt(sub: str = ""):
    iat = datetime.now(timezone.utc)
    message = TokenMessage(iss="music_storage_system", sub=sub, iat=get_int_from_datetime(iat),
                           exp=get_int_from_datetime(
                               iat + timedelta(minutes=5)))
    # A RSA key from a PEM file.
    with open(f'{get_project_root()}/private_key_for_testing_purposes.pem', 'rb') as fh:
        signing_key = jwk_from_pem(pem_content=fh.read())
    compact_jws = instance.encode(message.dict(), signing_key, alg='RS256')
    return compact_jws


def decode_jwt(jwt_token: str):
    with open(f'{get_project_root()}/public_key.json', 'r') as fh:
        verifying_key = jwk_from_dict(json.load(fh))

    message_received = instance.decode(
        jwt_token, verifying_key, do_time_check=True)
    return message_received


def get_project_root() -> Path:
    return Path(__file__).parent.parent
