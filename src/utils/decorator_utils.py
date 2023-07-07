from utils.jwt_utils import JWTUtils
from utils.schema.token_input import TokenInput


def encode_and_store_jwt(function):
    def wrapper(*args, **kwargs):
        token_input = function(*args, **kwargs)
        if isinstance(token_input, TokenInput):
            token = JWTUtils.encode_jwt(token_input)
            JWTUtils.store_jwt_in_config(token)
        return token_input
    return wrapper


def test(function):
    def wrapper(*args, **kwargs):
        token_input = function(*args, **kwargs)
        print("token_input")
        return token_input
    return wrapper