from unittest.mock import MagicMock, ANY

from sqlalchemy.engine import ScalarResult
from sqlmodel import Session

from models.user import User
from repositories.user_repository import UserRepository


def test_when_get_user_by_username_with_correct_id_then_user_is_returned():
    # Given
    mock_session = MagicMock(Session)

    mocked_scalar_res = MagicMock(ScalarResult)
    user_repo = UserRepository()
    ANY_USER_NAME = "test"
    mock_session.exec.return_value = mocked_scalar_res
    mocked_scalar_res.one.return_value = User(username=ANY_USER_NAME)

    # When
    user: User = user_repo.get_user_by_username(mock_session, ANY)

    # When
    assert user is not None
    assert user.username == ANY_USER_NAME
