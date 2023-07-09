from exceptions.user_denied_exception import UserDeniedError
from utils.jwt_utils import JWTUtils
from utils.schema.token import Token
from utils.schema.token_input import TokenInput
import os

def encode_and_store_jwt(function):
    def wrapper(*args, **kwargs):
        token_input = function(*args, **kwargs)
        if token_input == "access_denied":
            raise UserDeniedError("access_denied")
        if isinstance(token_input, TokenInput):
            token = JWTUtils.encode_jwt(token_input)
            JWTUtils.store_jwt_in_config(token)
            os.environ["music_app_token"] = token
        return token_input

    return wrapper


def check_token_and_role(role):
    def first_warapper(function):
        def wrapper(*args, **kwargs):
            token = os.environ.get("music_app_token")
            try:
                token_decoded: Token = JWTUtils.decode_jwt(token)
                if role not in token_decoded["permissions"]:
                    raise UserDeniedError("access_denied")
                res = function(*args, **kwargs)
                return res
            except UserDeniedError as e:
                raise e
            except Exception:
                raise UserDeniedError("access_denied")
        return wrapper
    return first_warapper
