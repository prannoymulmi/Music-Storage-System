import os
import sys

import typer

MINIMUM_USER_PASS_VALUE = 5
MAX_USER_PASS_VALUE = 50
MAX_FILE_NAME_LENGTH = 50
MAX_AUDIO_FILE_SIZE = 35000000  # 35 MB


class GeneralUtils:
    @staticmethod
    def sanitize_user_name_and_password_input(value):
        if len(value) > MAX_USER_PASS_VALUE or len(value) < MINIMUM_USER_PASS_VALUE:
            raise typer.BadParameter(
                f'The minimum value should be {MINIMUM_USER_PASS_VALUE} and maximum should be {MAX_USER_PASS_VALUE}')
        return value

    @staticmethod
    def sanitize_int_input(value: int):
        if value > sys.maxsize or value < 0:
            raise typer.BadParameter(
                f'The minimum value should be {0} and maximum should be {sys.maxsize}')
        return value

    @staticmethod
    def sanitize_audio_file_input(path: str):
        allowed_file_types_audio = [".mp3", ".aac", ".wav", ".wma", ".flac"]
        _, file_extension = os.path.splitext(path)
        filename = os.path.basename(path)
        if len(filename) > MAX_FILE_NAME_LENGTH:
            raise typer.BadParameter(
                f'The maximum value of the file name should be {MAX_FILE_NAME_LENGTH}')
        elif file_extension not in allowed_file_types_audio:
            raise typer.BadParameter(
                f'The file extension is not allowed')
        elif os.path.getsize(path) >= MAX_AUDIO_FILE_SIZE:
            raise typer.BadParameter(
                f'The max allowed size of audio file is  {MAX_AUDIO_FILE_SIZE / 1000000} MB')
        return path
