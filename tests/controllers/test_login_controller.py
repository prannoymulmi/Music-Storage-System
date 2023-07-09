from unittest import mock, TestCase
from unittest.mock import MagicMock, patch, ANY

import argon2
import pytest
from sqlmodel import Session

from exceptions.user_denied_exception import UserDeniedError
from models.role import Role
from models.role_names import RoleNames
from models.user import User
from repositories import user_repository, role_repository
from utils.schema.token_input import TokenInput

'''
The mock has to be patched before the login controller is imported so that the decorator mock is loaded.
If the mock is not done before importing then decorator is not mocked.
<a href=https://medium.com/@arlindont/python-unittest-mock-decorator-ab32c22a12ff/>
'''
def mock_decorator_encode_jwt(function):
    def wrapper(*args, **kwargs):
        res = function(*args, **kwargs)
        if res == "access_denied":
            return res
        return TokenInput(user_data=User(id=1), role=Role(id=1, role_name="test"))
    return wrapper


patch('utils.decorator_utils.encode_and_store_jwt', mock_decorator_encode_jwt).start()

def mock_decorator_check_token(role):
    def first_warapper(function):
        def wrapper(*args, **kwargs):
            res = function(*args, **kwargs)
            return res
        return wrapper

    return first_warapper


patch('utils.decorator_utils.check_token_and_role', mock_decorator_check_token).start()

# ruff: noqa: E402
from src.controllers.login_controller import LoginController


@mock.patch.object(user_repository.UserRepository, "update_user")
@mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
@mock.patch.object(user_repository.UserRepository, "get_user_by_username")
@mock.patch.object(argon2.PasswordHasher, "verify")
def test_login_when_password_correct_return_logged_in(
        mock_password_hasher, mock_user_repo, mock_role_repo, mock_user_repo_update_user
):
    # Given
    mock_password_hasher.return_value = True
    mock_user_repo.return_value = User(password="password")
    mock_role_repo.return_value = Role(id=1, role_name="ADMIN")

    # When
    login = LoginController()
    result = login.login("some_user", "password")

    # Then
    mock_user_repo_update_user.assert_called_once()
    assert isinstance(result, TokenInput)


@mock.patch.object(user_repository.UserRepository, "update_user")
@mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
@mock.patch.object(user_repository.UserRepository, "get_user_by_username")
@mock.patch.object(argon2.PasswordHasher, "verify")
def test_login_when_password_incorrect_return_access_denied(
        mock_password_hasher, mock_user_repo, mock_role_repo, mock_user_repo_update_user
):
    # Given
    mock_password_hasher.return_value = False
    mock_user_repo.return_value = User(password="password")
    mock_role_repo.return_value = Role(id=1, role_name="ADMIN")

    # When
    login = LoginController()
    result = login.login("some_user", "wrongPassword")
    # Then
    mock_user_repo_update_user.assert_called_once()
    assert result == "access_denied"


@mock.patch.object(user_repository.UserRepository, "create_user_or_else_return_none")
def test_login_when_add_new_user_with_known_role_then_return_new_user(
         mock_user_repo
):
    # Given
    mock_user_repo.return_value=True

    # When
    login_controller = LoginController()

    # Then
    login_controller.add_new_user(ANY, ANY, RoleNames.normal_user.value)
    mock_user_repo.assert_called_once()


@mock.patch.object(user_repository.UserRepository, "create_user_or_else_return_none")
def test_login_when_add_new_user_with_unknown_role_then_return_user_denied_error_with_role_not_found(
         mock_user_repo
):
    # Given
    mock_user_repo.return_value=True

    # When
    login_controller = LoginController()

    # Then
    with pytest.raises(UserDeniedError, match="role does not exist"):
        login_controller.add_new_user(ANY, ANY, "test")

    mock_user_repo.assert_not_called()