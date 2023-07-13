from unittest import mock

import pytest

import utils.jwt_utils
from exceptions.user_denied_exception import UserDeniedError
from exceptions.weak_password import WeakPasswordError
from models.role import Role
from models.user import User
from src.utils.decorator_utils import encode_and_store_jwt, check_token_and_role
from utils.schema.token import Token
from utils.schema.token_input import TokenInput


@mock.patch.object(utils.jwt_utils.JWTUtils, "encode_jwt")
@mock.patch.object(utils.jwt_utils.JWTUtils, "store_jwt_in_config")
def test_when_encode_and_store_jwt_then_token_is_create_and_stored(mock_store_jwt, mock_encoder):
    mock_encoder.return_value = "test"

    @encode_and_store_jwt
    def to_be_decorated():
        return TokenInput(user_data=User(), role=Role())
    to_be_decorated()
    mock_encoder.assert_called_once()
    mock_store_jwt.assert_called_once()
    # mock_store_jwt.assert_not_called()

@mock.patch.object(utils.jwt_utils.JWTUtils, "decode_jwt")
def test_when_check_token_and_role_when_role_is_present_then_function_is_called(mock_decoder):
    mock_decoder.return_value = Token(permissions=["TEST"])

    @check_token_and_role(role=["TEST"])
    def to_be_decorated():
        return "Running"
    # Then
    result = to_be_decorated()
    mock_decoder.assert_called_once()
    assert result in "Running"


@mock.patch.object(utils.jwt_utils.JWTUtils, "decode_jwt")
def test_when_check_token_and_role_when_multiple_roles_are_present_then_function_is_called(mock_decoder):
    mock_decoder.return_value = Token(permissions=["TEST2"])

    @check_token_and_role(role=["TEST", "TEST2"])
    def to_be_decorated():
        return "Running"
    # Then
    result = to_be_decorated()
    mock_decoder.assert_called_once()
    assert result in "Running"


@mock.patch.object(utils.jwt_utils.JWTUtils, "decode_jwt")
def test_when_check_token_and_role_when_role_is_not_present_then_function_is_not_called(mock_decoder):
    mock_decoder.return_value = Token(permissions=[""])

    @check_token_and_role(role=["TEST"])
    def to_be_decorated():
        return "Running"
    # Then
    with pytest.raises(UserDeniedError):
        to_be_decorated()
    mock_decoder.assert_called_once()

@mock.patch.object(utils.jwt_utils.JWTUtils, "decode_jwt")
def test_when_check_token_and_role_when_function_throws_weak_password_exception_present_then_wrapper_throws_it_back(mock_decoder):
    mock_decoder.return_value = Token(permissions=["TEST"])

    @check_token_and_role(role=["TEST"])
    def to_be_decorated():
        raise WeakPasswordError
    # Then
    with pytest.raises(WeakPasswordError):
        to_be_decorated()
    mock_decoder.assert_called_once()

@mock.patch.object(utils.jwt_utils.JWTUtils, "decode_jwt")
def test_when_check_token_and_role_when_function_throws_generic_exception_present_then_wrapper_throws_user_denied_error(mock_decoder):
    mock_decoder.return_value = Token(permissions=["TEST"])

    @check_token_and_role(role=["TEST"])
    def to_be_decorated():
        raise Exception
    # Then
    with pytest.raises(UserDeniedError):
        to_be_decorated()
    mock_decoder.assert_called_once()
