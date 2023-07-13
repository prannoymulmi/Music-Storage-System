from unittest.mock import MagicMock

from sqlalchemy.engine import ScalarResult
from sqlmodel import Session

from models.music_data import MusicData

MUSIC_DATA = MusicData(id=101, music_score=1, user_id=20)
from models.user import User
from repositories.music_repository import MusicRepository


def test_when_get_music_data_by_user_with_correct_user_then_the_correct_music_datas_are_returned():
    # Given
    mock_session = MagicMock(Session)

    mocked_scalar_res = MagicMock(ScalarResult)
    music_repo = MusicRepository()

    mock_session.exec.return_value = mocked_scalar_res
    mocked_scalar_res.all.return_value = [MusicData(id=1, music_score=1, user_id=20)]

    # When
    music_data_all: [MusicData] = music_repo.get_music_data_by_user(mock_session, User(id=20))

    # When
    mock_session.exec.assert_called_once()
    mocked_scalar_res.all.assert_called_once()
    assert music_data_all is not None
    assert music_data_all[0].music_score == 1
    assert music_data_all[0].id == 1

def test_when_get_music_data_by_music_id_with_correct_music_id_then_the_correct_music_data_is_returned():
    # Given
    mock_session = MagicMock(Session)

    mocked_scalar_res = MagicMock(ScalarResult)
    music_repo = MusicRepository()

    mock_session.exec.return_value = mocked_scalar_res
    mocked_scalar_res.one.return_value = MusicData(id=101, music_score=1, user_id=20)

    # When
    music_data_all: MusicData = music_repo.get_music_data_by_music_id(mock_session, 1)

    # When
    mock_session.exec.assert_called_once()
    mocked_scalar_res.one.assert_called_once()
    mocked_scalar_res.all.assert_not_called()
    assert music_data_all is not None
    assert music_data_all.music_score == 1
    assert music_data_all.id == 101


def test_when_update_music_data_with_correct_music_data_then_the_correct_music_data_is_updated():
    # Given
    mock_session = MagicMock(Session)

    mocked_scalar_res = MagicMock(ScalarResult)
    music_repo = MusicRepository()

    mock_session.exec.return_value = mocked_scalar_res
    mocked_scalar_res.one.return_value = MUSIC_DATA

    # When
    music_repo.update_music_data(mock_session, MUSIC_DATA)

    # When
    mock_session.exec.assert_called_once()
    mocked_scalar_res.one.assert_called_once()
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

def test_when_get_all_music_data_then_the_correct_music_datas_are_returned():
    # Given
    mock_session = MagicMock(Session)

    mocked_scalar_res = MagicMock(ScalarResult)
    music_repo = MusicRepository()

    mock_session.exec.return_value = mocked_scalar_res
    mocked_scalar_res.all.return_value = [MusicData(id=1, music_score=1, user_id=20)]

    # When
    music_repo.get_all_music_data(mock_session)

    # When
    mock_session.exec.assert_called_once()
    mocked_scalar_res.all.assert_called_once()

def test_when_create_and_add_new_music_data_then_the_correct_music_datas_are_created():
    # Given
    mock_session = MagicMock(Session)

    music_repo = MusicRepository()

    # When
    music_repo.create_and_add_new__music_data(mock_session, MUSIC_DATA)

    # When
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_when_delete_data_by_id_and_correct_id_then_the_correct_music_data_is_deleted():
    # Given
    mock_session = MagicMock(Session)

    music_repo = MusicRepository()

    # When
    music_repo.delete_data_by_id(mock_session, 1)

    # When
    mock_session.exec.assert_called_once()
    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()
