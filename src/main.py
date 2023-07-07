import warnings

import typer
from sqlmodel import Session
from typing_extensions import Annotated

from controllers.login_controller import LoginController
from factories.config_factory import ConfigFactory
from factories.controller_factory import ControllerFactory
from utils.schema.token_input import TokenInput

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
    result = controller.login(username, password, load_app_config())
    if isinstance(result, TokenInput) and result:
        print("logged_in")
    else:
        print("access_denied")

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
