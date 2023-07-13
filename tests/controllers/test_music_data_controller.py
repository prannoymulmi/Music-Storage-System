from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock

import pytest
from sqlmodel import Session

from controllers.music_data_controller import MusicDataController
from exceptions.user_denied_exception import UserDeniedError
from models.music_data import MusicData
from models.role import Role
from models.user import User
from repositories import music_repository, role_repository
from utils import configLoader, jwt_utils
from utils.music_utils import MusicUtils
from utils.schema.music_data_output import MusicDataOutput
from utils.schema.token import Token


@mock.patch.object(configLoader.ConfigLoader, "load_config")
@mock.patch.object(music_repository.MusicRepository, "create_and_add_new__music_data")
def test_add_music_data_when_correct_data_is_provided_then_the_data_is_uploaded_and_checksum_is_calculated(
        mock_music_repo, mock_config_loader
):
    mock_session = MagicMock(Session)

    mock_config_loader.return_value = mock_session

    music_data_controller: MusicDataController = MusicDataController()
    root_path: str = f"{Path(__file__).parent.parent.parent}"
    user = User(id=1)

    music_utils = MusicUtils.instance()

    music_file_path = f"{root_path}/audio_file_test.mp3"
    lyrics_file_path = f"{root_path}/test.txt"
    music_score = 100

    music_file = music_utils.get_file_from_path(music_file_path)
    lyrics_file = music_utils.get_file_from_path(lyrics_file_path)

    combined_check_sum = music_utils.calculate_check_sum(music_file + lyrics_file)
    music_data = MusicData(user_id=user.id,
                           music_file_name="audio_file_test.mp3",
                           music_file=music_file,
                           music_score=music_score,
                           checksum=combined_check_sum,
                           lyrics_file_name="test.txt",
                           lyrics=lyrics_file
                           )

    music_data_controller.add_music_data(music_file_path, music_score, lyrics_file_path, user)
    mock_music_repo.assert_has_calls(mock_session, music_data)


@mock.patch.object(jwt_utils.JWTUtils, "decode_jwt")
@mock.patch.object(configLoader.ConfigLoader, "load_config")
@mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
@mock.patch.object(music_repository.MusicRepository, "update_music_data")
@mock.patch.object(music_repository.MusicRepository, "get_music_data_by_music_id")
def test_update_music_data_when_role_is_normal_user_then_the_data_is_updated(
        mock_music_repo_get_music,
        mock_music_repo_update_music,
        mock_role_repo,
        mock_config_loader,
        mock_decode_jwt
):
    mock_session = MagicMock(Session)

    mock_config_loader.return_value = mock_session

    mock_decode_jwt.return_value = Token(permissions=["NORMAL_USER"])
    mock_role_repo.return_value = Role(id=2, role_name="NORMAL_USER")
    root_path: str = f"{Path(__file__).parent.parent.parent}"

    music_utils = MusicUtils.instance()

    music_file_path = f"{root_path}/audio_file_test.mp3"
    lyrics_file_path = f"{root_path}/test.txt"
    music_score = 100

    music_file = music_utils.get_file_from_path(music_file_path)
    lyrics_file = music_utils.get_file_from_path(lyrics_file_path)
    music_controller = MusicDataController()
    combined_check_sum = music_utils.calculate_check_sum(music_file + lyrics_file)
    user = User(id=1)
    music_data = MusicData(user_id=user.id,
                           music_file_name="audio_file_test.mp3",
                           music_file=music_file,
                           music_score=music_score,
                           checksum=combined_check_sum,
                           lyrics_file_name="test.txt",
                           lyrics=lyrics_file,
                           id=1
                           )

    mock_music_repo_get_music.return_value = music_data

    music_data_input = MusicDataOutput(id=1, music_score=1)

    music_data_updated = MusicData(user_id=user.id,
                           music_file_name="audio_file_test.mp3",
                           music_file=music_file,
                           music_score=1,
                           checksum=combined_check_sum,
                           lyrics_file_name="test.txt",
                           lyrics=lyrics_file,
                           id=1
                           )

    music_controller.update_music_data(user, music_data_input)
    mock_music_repo_update_music.assert_has_calls(mock_session, music_data_updated)


@mock.patch.object(jwt_utils.JWTUtils, "decode_jwt")
@mock.patch.object(configLoader.ConfigLoader, "load_config")
@mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
@mock.patch.object(music_repository.MusicRepository, "update_music_data")
@mock.patch.object(music_repository.MusicRepository, "get_music_data_by_music_id")
def test_update_music_data_when_role_is_normal_user_and_music_file_updated_then_the_data_is_updated_with_new_checksum(
        mock_music_repo_get_music,
        mock_music_repo_update_music,
        mock_role_repo,
        mock_config_loader,
        mock_decode_jwt
):
    mock_session = MagicMock(Session)

    mock_config_loader.return_value = mock_session
    mock_decode_jwt.return_value = Token(permissions=["NORMAL_USER"])
    mock_role_repo.return_value = Role(id=2, role_name="NORMAL_USER")
    root_path: str = f"{Path(__file__).parent.parent.parent}"

    music_utils = MusicUtils.instance()

    music_file_path = f"{root_path}/audio_file_test.mp3"
    lyrics_file_path = f"{root_path}/test.txt"
    music_score = 100

    music_file = music_utils.get_file_from_path(music_file_path)
    lyrics_file = music_utils.get_file_from_path(lyrics_file_path)
    music_controller = MusicDataController()
    combined_check_sum = music_utils.calculate_check_sum(music_file + lyrics_file)
    user = User(id=1)
    music_data = MusicData(user_id=user.id,
                           music_file_name="audio_file_test.mp3",
                           music_file=music_file,
                           music_score=music_score,
                           checksum=combined_check_sum,
                           lyrics_file_name="test.txt",
                           lyrics=lyrics_file,
                           id=1
                           )

    mock_music_repo_get_music.return_value = music_data

    music_data_input = MusicDataOutput(id=1, music_score=1)

    music_file_path_updated = f"{root_path}/audio_file_test_two.mp3"
    music_file_updated = music_utils.get_file_from_path(music_file_path_updated)
    new_check_sum = music_utils.calculate_check_sum(music_file_updated + lyrics_file)
    music_data_updated = MusicData(user_id=user.id,
                           music_file_name="audio_file_test_two.mp3",
                           music_file=music_file_updated,
                           music_score=1,
                           checksum=new_check_sum,
                           lyrics_file_name="test.txt",
                           lyrics=lyrics_file,
                           id=1
                           )

    music_controller.update_music_data(user, music_data_input)
    mock_music_repo_update_music.assert_has_calls(mock_session, music_data_updated)

@mock.patch.object(configLoader.ConfigLoader, "load_config")
@mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
@mock.patch.object(music_repository.MusicRepository, "update_music_data")
@mock.patch.object(music_repository.MusicRepository, "get_music_data_by_music_id")
def test_update_music_data_when_role_is_normal_user_and_user_id_does_not_match_then_the_data_is_not_updated_and_user_is_denied(
        mock_music_repo_get_music, mock_music_repo_update_music, mock_role_repo, mock_config_loader
):
    mock_session = MagicMock(Session)

    mock_config_loader.return_value = mock_session

    mock_role_repo.return_value = Role(id=2, role_name="NORMAL_USER")
    root_path: str = f"{Path(__file__).parent.parent.parent}"

    music_utils = MusicUtils.instance()

    music_file_path = f"{root_path}/audio_file_test.mp3"
    lyrics_file_path = f"{root_path}/test.txt"
    music_score = 100

    music_file = music_utils.get_file_from_path(music_file_path)
    lyrics_file = music_utils.get_file_from_path(lyrics_file_path)
    music_controller = MusicDataController()
    combined_check_sum = music_utils.calculate_check_sum(music_file + lyrics_file)
    not_the_same_user_id = 100
    user = User(id=not_the_same_user_id)
    music_data = MusicData(user_id=123,
                           music_file_name="audio_file_test.mp3",
                           music_file=music_file,
                           music_score=music_score,
                           checksum=combined_check_sum,
                           lyrics_file_name="test.txt",
                           lyrics=lyrics_file,
                           id=1
                           )

    mock_music_repo_get_music.return_value = music_data

    music_data_input = MusicDataOutput(id=1, music_score=1)

    with pytest.raises(UserDeniedError):
        music_controller.update_music_data(user, music_data_input)
    mock_music_repo_update_music.assert_not_called()


@mock.patch.object(jwt_utils.JWTUtils, "decode_jwt")
@mock.patch.object(configLoader.ConfigLoader, "load_config")
@mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
@mock.patch.object(music_repository.MusicRepository, "update_music_data")
@mock.patch.object(music_repository.MusicRepository, "get_music_data_by_music_id")
def test_update_music_data_when_role_is_Admin_and_different_user_id_then_the_data_is_updated_with_new_checksum(
        mock_music_repo_get_music,
        mock_music_repo_update_music,
        mock_role_repo,
        mock_config_loader,
        mock_decode_jwt
):
    mock_session = MagicMock(Session)

    mock_config_loader.return_value = mock_session
    mock_decode_jwt.return_value = Token(permissions=["ADMIN"])
    mock_role_repo.return_value = Role(id=2, role_name="ADMIN")
    root_path: str = f"{Path(__file__).parent.parent.parent}"

    music_utils = MusicUtils.instance()

    music_file_path = f"{root_path}/audio_file_test.mp3"
    lyrics_file_path = f"{root_path}/test.txt"
    music_score = 100

    music_file = music_utils.get_file_from_path(music_file_path)
    lyrics_file = music_utils.get_file_from_path(lyrics_file_path)
    music_controller = MusicDataController()
    combined_check_sum = music_utils.calculate_check_sum(music_file + lyrics_file)
    another_user_id = 101
    user = User(id=1)
    music_data = MusicData(user_id=another_user_id,
                           music_file_name="audio_file_test.mp3",
                           music_file=music_file,
                           music_score=music_score,
                           checksum=combined_check_sum,
                           lyrics_file_name="test.txt",
                           lyrics=lyrics_file,
                           id=1
                           )

    mock_music_repo_get_music.return_value = music_data

    music_data_input = MusicDataOutput(id=1, music_score=1)

    music_file_path_updated = f"{root_path}/audio_file_test_two.mp3"
    music_file_updated = music_utils.get_file_from_path(music_file_path_updated)
    new_check_sum = music_utils.calculate_check_sum(music_file_updated + lyrics_file)

    music_data_updated = MusicData(user_id=another_user_id,
                                   music_file_name="audio_file_test_two.mp3",
                                   music_file=music_file_updated,
                                   music_score=1,
                                   checksum=new_check_sum,
                                   lyrics_file_name="test.txt",
                                   lyrics=lyrics_file,
                                   id=1
                                   )

    music_controller.update_music_data(user, music_data_input)
    mock_music_repo_update_music.assert_has_calls(mock_session, music_data_updated)

@mock.patch.object(jwt_utils.JWTUtils, "decode_jwt")
@mock.patch.object(configLoader.ConfigLoader, "load_config")
@mock.patch.object(role_repository.RoleRepository, "get_role_by_id")
@mock.patch.object(music_repository.MusicRepository, "update_music_data")
@mock.patch.object(music_repository.MusicRepository, "get_music_data_by_music_id")
def test_update_music_data_when_role_is_normal_user_and_partial_music_file_updated_then_the_data_is_updated_with_new_checksum(
        mock_music_repo_get_music,
        mock_music_repo_update_music,
        mock_role_repo,
        mock_config_loader,
        mock_decode_jwt
):
    mock_session = MagicMock(Session)

    mock_config_loader.return_value = mock_session
    mock_decode_jwt.return_value = Token(permissions=["NORMAL_USER"])
    mock_role_repo.return_value = Role(id=2, role_name="NORMAL_USER")
    root_path: str = f"{Path(__file__).parent.parent.parent}"

    music_utils = MusicUtils.instance()

    music_file_path = f"{root_path}/audio_file_test.mp3"
    lyrics_file_path = f"{root_path}/test.txt"
    music_score = 100

    music_file = music_utils.get_file_from_path(music_file_path)
    lyrics_file = music_utils.get_file_from_path(lyrics_file_path)
    music_controller = MusicDataController()
    combined_check_sum = music_utils.calculate_check_sum(music_file + lyrics_file)
    user = User(id=1)
    music_data = MusicData(user_id=user.id,
                           music_file_name="audio_file_test.mp3",
                           music_file=music_file,
                           music_score=music_score,
                           checksum=combined_check_sum,
                           lyrics_file_name="test.txt",
                           lyrics=lyrics_file,
                           id=1
                           )

    mock_music_repo_get_music.return_value = music_data



    music_file_path_updated = f"{root_path}/audio_file_test_two.mp3"
    music_file_updated = music_utils.get_file_from_path(music_file_path_updated)
    new_check_sum = music_utils.calculate_check_sum(music_file_updated + lyrics_file)
    music_data_input = MusicData(id=1,
                                 music_score=1,
                                 music_file_name=music_file_path_updated)
    music_data_updated = MusicData(user_id=user.id,
                           music_file_name="audio_file_test_two.mp3",
                           music_file=music_file_updated,
                           music_score=1,
                           checksum=new_check_sum,
                           lyrics_file_name="test.txt",
                           lyrics=lyrics_file,
                           id=1
                           )

    music_controller.update_music_data(user, music_data_input)
    mock_music_repo_update_music.assert_has_calls(mock_session, music_data_updated)