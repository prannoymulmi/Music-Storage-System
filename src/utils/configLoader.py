import os
import uuid
from pathlib import Path

import typer

from configs.db_config import create_db_and_tables, get_session


class ConfigLoader:
    APP_NAME = os.path.abspath(__file__)

    def __init__(self) -> None:
        super().__init__()

    def load_config(self):
        create_db_and_tables()
        app_dir = typer.get_app_dir(self.APP_NAME)
        config_path: Path = Path(app_dir).parents[2] / "music_storage_system_config"
        config_path_key: Path = Path(app_dir).parents[2] / "keys_config"
        if config_path.is_file():
            file = open(config_path, "r")
            line = file.readline()
            os.environ["music_app_token"] = line.split("token:")[1]
        if config_path_key.is_file():
            file = open(config_path_key, "r")
            line = file.readline()
            os.environ["encryption_key"] = line.split("ENCRYPTION_KEY:")[1]
        else:
            file = open(config_path_key, "w")
            key = str(uuid.uuid4())
            file.write(f'ENCRYPTION_KEY:{uuid.uuid4()}')
            os.environ["encryption_key"] = key
        return get_session()
