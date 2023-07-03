from sqlmodel import Session
from typing_extensions import Annotated

import typer
import warnings
from factories.config_factory import ConfigFactory
from factories.controller_factory import ControllerFactory
from controllers.login_controller import LoginController

app = typer.Typer()
warnings.filterwarnings("ignore")

# @click.group()
# def cli():
#     load_app_config()
#     pass
session = None
@app.command()
def login(username: Annotated[str, typer.Option(prompt=True)],
          password: Annotated[str, typer.Option(prompt=True, hide_input=True)]):
    controller: LoginController = ControllerFactory().create_object("login_controller")
    controller.login(username, password, load_app_config())
    print("login")


@app.command()
def add_music_data():
    pass
    # click.echo("Dropped the database")


@app.command()
def list_music_data():
    print("Listing")


@app.command()
def delete_music_data():
    print("deleting")


def load_app_config() -> Session:
    loader = ConfigFactory().create_object('config_loader')
    session_from_config = loader.load_config()
    return session_from_config


def main():
    load_app_config()
    app()


if __name__ == "__main__":
    main()
