from typing_extensions import Annotated

import typer

from factories.config_factory import ConfigFactory
from factories.controller_factory import ControllerFactory
from controllers.login_controller import LoginController

app = typer.Typer()


# @click.group()
# def cli():
#     load_app_config()
#     pass

@app.command()
def login(username: Annotated[str, typer.Option(prompt=True)],
          password: Annotated[str, typer.Option(prompt=True, hide_input=True)]):
    controller: LoginController = ControllerFactory().create_object("login_controller")
    print(controller.login(username, password))
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


def load_app_config():
    loader = ConfigFactory().create_object('config_loader')
    loader.load_config()


def main():
    load_app_config()
    app()


if __name__ == "__main__":
    main()
