from unittest import mock
from unittest.mock import MagicMock

from sqlmodel import Session

from models.user import User
from repositories import user_repository
from src.controllers.login_controller import LoginController


@mock.patch.object(user_repository.UserRepository, "get_user_id")
def test_login(mock_user_repo):
    mock_user_repo.return_value = User(password="password")
    mock_session = MagicMock(Session)
    login = LoginController()
    result = login.login("some_user", "password", mock_session)
    assert result == "logged in"

