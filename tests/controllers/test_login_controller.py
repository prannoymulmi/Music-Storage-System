import os
import unittest
from datetime import datetime, timedelta
from unittest import mock
from unittest.mock import patch, ANY

import argon2
import pytest
from argon2.exceptions import VerifyMismatchError

from exceptions.jwt_decode_error import JWTDecodeError
from exceptions.user_denied_exception import UserDeniedError
from exceptions.user_not_found import UserNotFound
from exceptions.weak_password import WeakPasswordError
from models.role import Role
from models.role_names import RoleNames
from models.user import User
from repositories import user_repository, role_repository
from tests.test_config import session_fixture
from utils import password_utils, jwt_utils, configLoader, encryption_utils
from utils.schema.token import Token
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

class TestLoginController(unittest.TestCase):

    def setUp(self):
        # Using in memory database for tests.
        self.mock_config = mock.patch.object(
            configLoader.ConfigLoader, 'load_config', return_value=session_fixture()
        )

    @mock.patch.object(user_repository.UserRepository, "update_user")
    @mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
    @mock.patch.object(user_repository.UserRepository, "get_user_by_username")
    @mock.patch.object(argon2.PasswordHasher, "verify")
    def test_login_when_password_correct_return_logged_in(
            self,
            mock_password_hasher,
            mock_user_repo,
            mock_role_repo,
            mock_user_repo_update_user
    ):
        with self.mock_config:
            # Given
            mock_password_hasher.return_value = True
            mock_user_repo.return_value = User(password="password", login_counter=0, last_login_attempt=datetime.utcnow())
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
            self,
            mock_password_hasher,
            mock_user_repo,
            mock_role_repo,
            mock_user_repo_update_user
    ):
        with self.mock_config:
            # Given
            mock_password_hasher.return_value = False
            mock_user_repo.return_value = User(password="password", login_counter=0, last_login_attempt=datetime.utcnow())
            mock_role_repo.return_value = Role(id=1, role_name="ADMIN")

            # When
            login = LoginController()
            with pytest.raises(UserDeniedError, match="access_denied"):
                login.login("some_user", "wrongPassword")
            # Then
            mock_user_repo_update_user.assert_called_once()

    @mock.patch.object(user_repository.UserRepository, "update_user")
    @mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
    @mock.patch.object(user_repository.UserRepository, "get_user_by_username")
    @mock.patch.object(argon2.PasswordHasher, "verify")
    def test_login_when_password_incorrect_with_hash_throwing_error_return_access_denied(
            self,
            mock_password_hasher,
            mock_user_repo,
            mock_role_repo,
            mock_user_repo_update_user
    ):
        with self.mock_config:
            # Given
            mock_password_hasher.side_effect = VerifyMismatchError
            mock_user_repo.return_value = User(password="password", login_counter=0, last_login_attempt=datetime.utcnow())
            mock_role_repo.return_value = Role(id=1, role_name="ADMIN")

            # When
            login = LoginController()
            with pytest.raises(UserDeniedError, match="access_denied"):
                login.login("some_user", "wrongPassword")
            # Then
            mock_user_repo_update_user.assert_called_once()

    @mock.patch.object(user_repository.UserRepository, "get_user_by_username")
    def test_login_when_password_incorrect_return_user_denied_error(
            self,
            mock_user_repo
    ):
        with self.mock_config:
            # Given
            mock_user_repo.side_effect = UserNotFound

            # When
            login = LoginController()
            with pytest.raises(UserDeniedError, match="Username or password is wrong"):
                login.login("some_user", "wrongPassword")
            # Then
            mock_user_repo.assert_called_once()

    @mock.patch.object(user_repository.UserRepository, "update_user")
    @mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
    @mock.patch.object(user_repository.UserRepository, "get_user_by_username")
    @mock.patch.object(argon2.PasswordHasher, "verify")
    def test_login_when_password_correct_but_login_counter_limit_exceeded_return_access_denied(
            self,
            mock_password_hasher,
            mock_user_repo,
            mock_role_repo,
            mock_user_repo_update_user
    ):
        with self.mock_config:
            # Given
            mock_user_repo.return_value = User(password="password", login_counter=6, last_login_attempt=datetime.utcnow())

            # When
            login = LoginController()
            with pytest.raises(UserDeniedError, match="User is blocked"):
                login.login("some_user", "wrongPassword")
            # Then
            mock_password_hasher.assert_not_called()
            mock_role_repo.assert_not_called()
            mock_user_repo_update_user.assert_not_called()
            mock_user_repo.assert_called_once()

    @mock.patch.object(user_repository.UserRepository, "update_user")
    @mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
    @mock.patch.object(user_repository.UserRepository, "get_user_by_username")
    @mock.patch.object(argon2.PasswordHasher, "verify")
    def test_login_when_password_correct_but_login_counter_limit_exceeded_and_time_limit_crossed_return_logged_in(
            self,
            mock_password_hasher,
            mock_user_repo,
            mock_role_repo,
            mock_user_repo_update_user
    ):
        with self.mock_config:
            # Given
            mock_password_hasher.return_value = True
            now = datetime.utcnow()
            td = timedelta(minutes=12)
            res = now - td
            mock_user_repo.return_value = User(password="password", login_counter=6, last_login_attempt=res)
            mock_role_repo.return_value = Role(id=1, role_name="ADMIN")

            # When
            login = LoginController()
            result = login.login("some_user", "password")

            # Then
            mock_password_hasher.assert_called_once()
            mock_role_repo.assert_called_once()
            mock_user_repo_update_user.assert_called_once()
            assert isinstance(result, TokenInput)

    @mock.patch.object(password_utils.PasswordUtil, "is_password_policy_non_compliant")
    @mock.patch.object(password_utils.PasswordUtil, "is_password_compromised_password_in_have_i_been_pawned")
    @mock.patch.object(user_repository.UserRepository, "create_user_or_else_return_none")
    def test_login_when_add_new_user_with_known_role_then_return_new_user(
            self,
            mock_user_repo,
            mock_password_util,
            mock_password_util_password_check
    ):
        with self.mock_config:
            # Given
            mock_user_repo.return_value = True
            mock_password_util.return_value = False
            mock_password_util_password_check.return_value = False

            # When
            login_controller = LoginController()

            # Then
            login_controller.add_new_user(ANY, ANY, RoleNames.normal_user.value)
            mock_user_repo.assert_called_once()

    @mock.patch.object(password_utils.PasswordUtil, "is_password_policy_non_compliant")
    @mock.patch.object(password_utils.PasswordUtil, "is_password_compromised_password_in_have_i_been_pawned")
    @mock.patch.object(user_repository.UserRepository, "create_user_or_else_return_none")
    def test_login_when_add_new_user_with_non_compliant_password_then_return_weak_password_error(
            self,
            mock_user_repo,
            mock_password_util,
            mock_password_util_pass_strength
    ):
        with self.mock_config:
            # Given
            mock_user_repo.return_value = True
            mock_password_util.return_value = False
            mock_password_util_pass_strength.return_value = True

            # When
            login_controller = LoginController()

            # Then
            with pytest.raises(WeakPasswordError, match="password is non-compliant"):
                login_controller.add_new_user(ANY, ANY, RoleNames.normal_user.value)
            mock_user_repo.assert_not_called()

    @mock.patch.object(password_utils.PasswordUtil, "is_password_compromised_password_in_have_i_been_pawned")
    @mock.patch.object(user_repository.UserRepository, "create_user_or_else_return_none")
    def test_login_when_add_new_user_with_non_have_i_been_pawned_compliant_password_then_return_weak_password_error(
            self,
            mock_user_repo,
            mock_password_util,
    ):
        with self.mock_config:
            # Given
            mock_user_repo.return_value = True
            mock_password_util.return_value = True

            # When
            login_controller = LoginController()

            # Then
            with pytest.raises(WeakPasswordError, match="Error: Have I been pawned says the password is compromised"):
                login_controller.add_new_user(ANY, ANY, RoleNames.normal_user.value)
            mock_user_repo.assert_not_called()

    @mock.patch.object(user_repository.UserRepository, "create_user_or_else_return_none")
    def test_login_when_add_new_user_with_unknown_role_then_return_user_denied_error_with_role_not_found(
            self,
            mock_user_repo
    ):
        with self.mock_config:
            # Given
            mock_user_repo.return_value = True

            # When
            login_controller = LoginController()

            # Then
            with pytest.raises(UserDeniedError, match="role does not exist"):
                login_controller.add_new_user(ANY, ANY, "test")

            mock_user_repo.assert_not_called()

    @mock.patch.object(encryption_utils.EncryptionUtils, "decrypt")
    @mock.patch.object(os.environ, "get")
    @mock.patch.object(jwt_utils.JWTUtils, "decode_jwt")
    @mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
    @mock.patch.object(user_repository.UserRepository, "get_user_by_user_id")
    def test_get_details_for_token_when_token_is_correct_then_token_input_is_returned(
            self,
            mock_user_repo,
            mock_role_repo,
            mock_jwt,
            mock_os,
            mock_decrypt
    ):
        with self.mock_config:
            mock_os.return_value = "some_token"
            mock_decrypt.return_value = "some_token"
            mock_jwt.return_value = Token(user_id=1, permissions=["TEST_Permissions"])
            user = User(role_id=1)
            mock_user_repo.return_value = user
            role = Role(role_name="TEST")
            mock_role_repo.return_value = role
            expected = TokenInput(user_data=user, role=role)

            login_controller = LoginController()

            result = login_controller.get_details_for_token()

            assert result == expected

    @mock.patch.object(encryption_utils.EncryptionUtils, "decrypt")
    @mock.patch.object(os.environ, "get")
    @mock.patch.object(jwt_utils.JWTUtils, "decode_jwt")
    @mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
    @mock.patch.object(user_repository.UserRepository, "get_user_by_user_id")
    def test_get_details_for_token_when_jwt_has_error_is_correct_then_user_denied_is_returned(
            self,
            mock_user_repo,
            mock_role_repo,
            mock_jwt,
            mock_os,
            mock_decrypt
    ):
        with self.mock_config:
            mock_os.return_value = "some_token"
            mock_jwt.side_effect = JWTDecodeError
            mock_decrypt.return_value = "some_token"

            login_controller = LoginController()

            with pytest.raises(UserDeniedError, match="Credentials expired"):
                login_controller.get_details_for_token()

            mock_user_repo.assert_not_called()
            mock_role_repo.assert_not_called()

    @mock.patch.object(os.environ, "get")
    @mock.patch.object(jwt_utils.JWTUtils, "decode_jwt")
    @mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
    @mock.patch.object(user_repository.UserRepository, "get_user_by_user_id")
    def test_get_details_for_token_when_exception_is_correct_then_user_denied_is_returned(
            self,
            mock_user_repo,
            mock_role_repo,
            mock_jwt,
            mock_os
    ):
        with self.mock_config:
            mock_os.return_value = "some_token"
            mock_jwt.side_effect = Exception


            login_controller = LoginController()

            with pytest.raises(UserDeniedError, match="access_denied"):
                login_controller.get_details_for_token()

            mock_user_repo.assert_not_called()
            mock_role_repo.assert_not_called()
