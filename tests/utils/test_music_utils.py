import builtins
from pathlib import Path
from unittest import mock

import pytest

from exceptions.data_not_found import DataNotFoundError
from exceptions.virus_found import VirusFoundError
from utils import music_utils
from utils.music_utils import MusicUtils


def test_music_util_is_singleton():
    instance = MusicUtils.instance()
    assert isinstance(instance, MusicUtils)


def test_music_util_is_throws_error_if_tried_to_create_object():
    with pytest.raises(RuntimeError):
        MusicUtils()


def test_get_file_name_from_path_none_then_empty_is_returned():
    result = MusicUtils.get_file_name_from_path(None)
    assert result == ""


def test_get_file_from_path_none_then_then_data_not_found_is_returned():
    with pytest.raises(DataNotFoundError):
        MusicUtils.get_file_from_path(None)


@mock.patch.object(builtins, "open")
def test_get_file_from_path_has_exception_then_data_not_found_is_returned(mock_open):
    mock_open.side_effect = Exception
    with pytest.raises(DataNotFoundError):
        MusicUtils.get_file_from_path(None)


@mock.patch.object(builtins, "open")
def test_write_file_from_path_has_exception_then_data_not_found_is_returned(mock_open):
    mock_open.side_effect = Exception
    with pytest.raises(DataNotFoundError):
        MusicUtils.write_bytes_to_file(b'00', "some_file")


@mock.patch.object(music_utils.MusicUtils, "scan_file")
def test_scan_file(mock_scan):
    mock_scan.side_effect = VirusFoundError("")
    valid_file_name = f"{Path(__file__).parent.parent}/files/EICAR-clamav-testfile.mp3"
    with pytest.raises(VirusFoundError):
        MusicUtils.scan_file(valid_file_name)
