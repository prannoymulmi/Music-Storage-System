import os
from pathlib import Path
import typer

class ConfigLoader:
    APP_NAME = os.path.abspath(__file__)

    def __init__(self) -> None:
        super().__init__()

    def load_config(self):
        app_dir = typer.get_app_dir(self.APP_NAME)
        config_path: Path = Path(app_dir).parents[2] / "config.json"
        if not config_path.is_file():
            print("Config file doesn't exist yet")
        return config_path
