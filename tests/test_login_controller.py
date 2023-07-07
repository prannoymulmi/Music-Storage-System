from unittest import mock
from unittest.mock import MagicMock, patch

import argon2
from sqlmodel import Session

from models.role import Role
from models.user import User
from repositories import user_repository, role_repository
from utils.schema.token_input import TokenInput

'''
The mock has to be patched before the login controller is imported so that the decorator mock is loaded.
If the mock is not done before importing then decorator is not mocked.
'''
def mock_decorator(function):
    def wrapper(*args, **kwargs):
        return TokenInput(user_data=User(id=1), role=Role(id=1, role_name="test"))
    return wrapper


patch('utils.decorator_utils.encode_and_store_jwt', mock_decorator).start()

# ruff: noqa: E402
from src.controllers.login_controller import LoginController


@mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
@mock.patch.object(user_repository.UserRepository, "get_user_id")
@mock.patch.object(argon2.PasswordHasher, "verify")
def test_login_when_password_correct_return_logged_in(
        mock_password_hasher, mock_user_repo, mock_role_repo
):
    # Given
    mock_session = MagicMock(Session)
    mock_password_hasher.return_value = True
    mock_user_repo.return_value = User(password="password")
    mock_role_repo.return_value = Role(id=1, role_name="ADMIN")

    # When
    login = LoginController()
    result = login.login("some_user", "password", mock_session)

    # Then
    assert isinstance(result, TokenInput)
