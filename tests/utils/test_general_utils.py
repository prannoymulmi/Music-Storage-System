import sys
from pathlib import Path

import pytest
import typer

from utils.general_utils import GeneralUtils, MAX_FILE_NAME_LENGTH, MINIMUM_USER_PASS_VALUE, MAX_USER_PASS_VALUE, \
    MAX_AUDIO_FILE_SIZE, MAX_LYRICS_FILE_SIZE


def test_sanitize_user_name_and_password_input_with_correct_value_then_string_is_returned():
    valid_string = "username1"
    result = GeneralUtils.sanitize_user_name_and_password_input(valid_string)
    assert result == valid_string


def test_sanitize_user_name_and_password_input_with_long_value_then_typer_error_is_returned():
    invalid_string = "VeryVeryLongTextVeryVeryLongTextVeryVeryLongTextVeryVeryLongTextVeryVeryLongTextVeryVeryLongTextVeryVeryLongText"
    with pytest.raises(typer.BadParameter,
                       match=f'The minimum value should be {MINIMUM_USER_PASS_VALUE} and maximum should be {MAX_USER_PASS_VALUE}'):
        GeneralUtils.sanitize_user_name_and_password_input(invalid_string)


def test_sanitize_int_input_with_correct_value_then_string_is_returned():
    valid_int = 500000
    result = GeneralUtils.sanitize_int_input(valid_int)
    assert result == valid_int


def test_sanitize_int_input_with_long_value_then_typer_error_is_returned():
    invalid_int = sys.maxsize + 1
    with pytest.raises(typer.BadParameter,
                       match=f'The minimum value should be {0} and maximum should be {sys.maxsize}'):
        GeneralUtils.sanitize_int_input(invalid_int)


def test_sanitize_audio_file_input_with_correct_value_then_string_is_returned():
    valid_file_name = f"{Path(__file__).parent.parent}/files/audio_file_test.mp3"
    result = GeneralUtils.sanitize_music_file_input(valid_file_name)
    assert result == valid_file_name


def test_sanitize_audio_file_with_long_value_then_typer_error_is_returned():
    invalid_file_name = "../files/audio_file_long_name_long_name_long_name_long_name_long_name_long_name_long_name_long_name.mp3"
    with pytest.raises(typer.BadParameter,
                       match=f'The maximum value of the file name should be {MAX_FILE_NAME_LENGTH}'):
        GeneralUtils.sanitize_music_file_input(invalid_file_name)


def test_sanitize_audio_file_with_large_file_then_typer_error_is_returned():
    invalid_file_name = f"{Path(__file__).parent.parent}/files/large_file.flac"
    with pytest.raises(typer.BadParameter,
                       match=f'The max allowed size of audio file is  {MAX_AUDIO_FILE_SIZE / 1000000} MB'):
        GeneralUtils.sanitize_music_file_input(invalid_file_name)


def test_sanitize_audio_file_with_forbidden_extension_then_typer_error_is_returned():
    invalid_file_name = f"{Path(__file__).parent.parent}/files/large_file.zip"
    with pytest.raises(typer.BadParameter,
                       match='The file extension is not allowed'):
        GeneralUtils.sanitize_music_file_input(invalid_file_name)


def test_sanitize_lyrics_file_input_with_correct_value_then_string_is_returned():
    valid_file_name = f"{Path(__file__).parent.parent}/files/lyrics_1.lrc"
    result = GeneralUtils.sanitize_lyrics_file_input(valid_file_name)
    assert result == valid_file_name


def test_sanitize_lyrics_file_with_long_value_then_typer_error_is_returned():
    invalid_file_name = "../files/lyrics_file_long_name_long_name_long_name_long_name_long_name_long_name_long_name_long_name.lrc"
    with pytest.raises(typer.BadParameter,
                       match=f'The maximum value of the file name should be {MAX_FILE_NAME_LENGTH}'):
        GeneralUtils.sanitize_lyrics_file_input(invalid_file_name)


def test_sanitize_lyrics_file_with_large_file_then_typer_error_is_returned():
    invalid_file_name = f"{Path(__file__).parent.parent}/files/large_lrc_file.lrc"
    with pytest.raises(typer.BadParameter,
                       match=f'The max allowed size of audio file is  {MAX_LYRICS_FILE_SIZE / 1000000} MB'):
        GeneralUtils.sanitize_lyrics_file_input(invalid_file_name)


def test_sanitize_lyrics_file_with_forbidden_extension_then_typer_error_is_returned():
    invalid_file_name = f"{Path(__file__).parent.parent}/files/large_file.zip"
    with pytest.raises(typer.BadParameter,
                       match='The file extension is not allowed'):
        GeneralUtils.sanitize_lyrics_file_input(invalid_file_name)
