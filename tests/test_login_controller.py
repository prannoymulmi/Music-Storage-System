from unittest import mock
from unittest.mock import MagicMock

import argon2
from sqlmodel import Session

from models.user import User
from repositories import user_repository
from src.controllers.login_controller import LoginController


@mock.patch.object(user_repository.UserRepository, "get_user_id")
@mock.patch.object(argon2.PasswordHasher, "verify")
def test_login_when_password_correct_return_logged_in(
        mock_password_hasher, mock_user_repo
):
    mock_session = MagicMock(Session)
    mock_password_hasher.return_value = True
    mock_user_repo.return_value = User(password="password")
    login = LoginController()
    result = login.login("some_user", "password", mock_session)
    assert result == "logged in"

