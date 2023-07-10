from pathlib import Path
from unittest import mock
from unittest.mock import ANY, MagicMock

from sqlmodel import Session

from controllers.music_data_controller import MusicDataController
from models.music_data import MusicData
from models.user import User
from repositories import music_repository
from utils import configLoader
from utils.music_utils import MusicUtils


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

    combined_check_sum = music_utils.calculate_check_sum(music_file+lyrics_file)
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