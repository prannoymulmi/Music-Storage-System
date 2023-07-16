import os
import secrets
from pathlib import Path

import typer

from configs.db_config import create_db_and_tables, get_session
from utils.music_utils import MusicUtils


class ConfigLoader:
    APP_NAME = os.path.abspath(__file__)

    def __init__(self) -> None:
        super().__init__()

    def load_config(self):
        create_db_and_tables()
        app_dir = typer.get_app_dir(self.APP_NAME)
        config_path: Path = Path(app_dir).parents[2] / "music_storage_system_config"
        random_byte_string_key = "test"
        os.environ["encryption_key"] = random_byte_string_key
        if config_path.is_file():
            file = open(config_path, "r")
            line = file.readline()
            os.environ["music_app_token"] = line.split("token:")[1]
        return get_session()

