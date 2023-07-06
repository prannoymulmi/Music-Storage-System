from utils.jwt_utils import JWTUtils


def encode_and_store_jwt(function):
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        if result in "logged in":
            token = JWTUtils.encode_jwt()
            JWTUtils.store_jwt_in_config(token)
        return result
    return wrapper