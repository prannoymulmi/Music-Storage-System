from unittest.mock import MagicMock

from sqlalchemy.engine import ScalarResult
from sqlmodel import Session

from models.music_data import MusicData
from models.role import Role
from repositories.role_repository import RoleRepository

MUSIC_DATA = MusicData(id=101, music_score=1, user_id=20)

def test_when_get_role_by_id_and_correct_id_then_role_is_returned():
    # Given
    mock_session = MagicMock(Session)

    role_repo = RoleRepository()
    mocked_scalar_res = MagicMock(ScalarResult)
    mocked_scalar_res.one.return_value = Role(id=1)
    mock_session.exec.return_value = mocked_scalar_res

    # When
    role_repo.get_role_by_id(mock_session, 1)

    # When
    mock_session.exec.assert_called_once()
    mocked_scalar_res.one.assert_called_once()


def test_create_and_add_role_then_role_is_created():
    # Given
    mock_session = MagicMock(Session)

    role_repo = RoleRepository()
    # When
    role_repo.create_and_add_role(mock_session, Role())

    # When
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
