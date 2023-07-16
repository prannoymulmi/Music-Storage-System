import os
import secrets
from unittest import mock
from unittest.mock import MagicMock, ANY

import pytest
from sqlalchemy.engine import ScalarResult
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from exceptions.user_not_found import UserNotFound
from models.role import Role
from models.user import User
from repositories import user_repository
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


def test_when_get_user_by_username_with_no_result_found_then_user_not_found_raised():
    # Given
    mock_session = MagicMock(Session)

    mocked_scalar_res = MagicMock(ScalarResult)
    user_repo = UserRepository()
    mock_session.exec.return_value = mocked_scalar_res
    mocked_scalar_res.one.side_effect = NoResultFound

    # When
    with pytest.raises(UserNotFound, match="User is not found"):
        user_repo.get_user_by_username(mock_session, ANY)


def test_when_get_user_by_id_with_correct_id_then_user_is_returned():
    # Given
    mock_session = MagicMock(Session)

    mocked_scalar_res = MagicMock(ScalarResult)
    user_repo = UserRepository()
    ANY_USER_ID = 1

    mock_session.exec.return_value = mocked_scalar_res
    user_id = "ANY_USER_ID"
    mocked_scalar_res.one.return_value = User(username=user_id, id=ANY_USER_ID)

    # When
    user: User = user_repo.get_user_by_user_id(mock_session, ANY)

    # When
    assert user is not None
    assert user.id == ANY_USER_ID


def test_when_get_user_by_id_with_no_result_found_then_user_not_found_raised():
    # Given
    mock_session = MagicMock(Session)

    mocked_scalar_res = MagicMock(ScalarResult)
    user_repo = UserRepository()
    ANY_USER_ID = 1

    mock_session.exec.return_value = mocked_scalar_res
    user_id = "ANY_USER_ID"
    mocked_scalar_res.one.return_value = User(username=user_id, id=ANY_USER_ID)

    # When
    mock_session.exec.return_value = mocked_scalar_res
    mocked_scalar_res.one.side_effect = NoResultFound

    # When
    with pytest.raises(UserNotFound, match="User is not found"):
        user_repo.get_user_by_user_id(mock_session, ANY)

@mock.patch.object(os.environ, "get")
def test_update_user_when_correct_details_then_is_updated(mock_os):
    mock_session = MagicMock(Session)

    user_repo = UserRepository()

    user_repo.update_user(mock_session, ANY)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_when_check_if_user_exists_with_no_result_found_then_return_false():
    # Given
    mock_session = MagicMock(Session)

    mocked_scalar_res = MagicMock(ScalarResult)
    user_repo = UserRepository()

    mock_session.exec.return_value = mocked_scalar_res

    # When
    mock_session.exec.return_value = mocked_scalar_res
    mocked_scalar_res.one.side_effect = NoResultFound

    # When
    result = user_repo.check_if_user_exists(ANY, mock_session)

    assert not result


def test_when_check_if_user_exists_then_return_true():
    # Given
    mock_session = MagicMock(Session)

    mocked_scalar_res = MagicMock(ScalarResult)
    user_repo = UserRepository()
    ANY_USER_ID = 1

    mock_session.exec.return_value = mocked_scalar_res
    user_id = "ANY_USER_ID"
    mocked_scalar_res.one.return_value = User(username=user_id, id=ANY_USER_ID)

    # When
    mock_session.exec.return_value = mocked_scalar_res

    # When
    result = user_repo.check_if_user_exists(ANY, mock_session)

    assert result


@mock.patch.object(user_repository.UserRepository, "check_if_user_exists")
def test_when_create_user_or_else_return_none__and_user_does_not_exist_then_user_is_created(
        mock_user_exist
):
    # Given
    mock_session = MagicMock(Session)

    mocked_scalar_res = MagicMock(ScalarResult)
    user_repo = UserRepository()

    mock_user_exist.return_value = False
    mock_session.exec.return_value = mocked_scalar_res
    mocked_scalar_res.one.return_value = Role(id=1)

    # When
    mock_session.exec.return_value = mocked_scalar_res

    # When
    result = user_repo.create_user_or_else_return_none(mock_session, "any_user", "any_pass", "any_role")

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert result is not None