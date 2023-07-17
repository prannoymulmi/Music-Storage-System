import os

from exceptions.data_not_found import DataNotFoundError
from exceptions.user_denied_exception import UserDeniedError
from exceptions.weak_password import WeakPasswordError
from utils.jwt_utils import JWTUtils
from utils.schema.token import Token
from utils.schema.token_input import TokenInput


def encode_and_store_jwt(function):
    def wrapper(*args, **kwargs):
        token_input = function(*args, **kwargs)
        if isinstance(token_input, TokenInput):
            token = JWTUtils.encode_jwt(token_input)
            JWTUtils.store_jwt_in_config(token)
            os.environ["music_app_token"] = token
        return token_input

    return wrapper


def check_token_and_role(role: [str]):
    def first_warapper(function):
        def wrapper(*args, **kwargs):
            try:
                token = os.environ.get("music_app_token")
                token_decoded: Token = JWTUtils.decode_jwt(token)
                if any(x in token_decoded.permissions for x in role):
                    res = function(*args, **kwargs)
                    return res
                raise UserDeniedError("access_denied")
            except UserDeniedError as e:
                raise e
            except WeakPasswordError as e:
                raise e
            except DataNotFoundError as e:
                raise e
            except Exception:
                ''' If the token is expired or has been the user will be be denied access'''
                raise UserDeniedError("access_denied")
        return wrapper
    return first_warapper
