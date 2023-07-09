import os

import typer
from sqlmodel import Session
from typing_extensions import Annotated

from controllers.login_controller import LoginController
from exceptions.user_denied_exception import UserDeniedError
from factories.config_factory import ConfigFactory
from factories.controller_factory import ControllerFactory
from models.role_names import RoleNames
from utils.schema.token_input import TokenInput

app = typer.Typer()

session = None


@app.command()
def login(username: Annotated[str, typer.Option(prompt=True)],
          password: Annotated[str, typer.Option(prompt=True, hide_input=True)]):
    controller: LoginController = ControllerFactory().create_object("login_controller")
    try:
        result = controller.login(username, password)
        if isinstance(result, TokenInput) and result:
            print("logged_in")
    except UserDeniedError as e:
        print(e.message)


@app.command()
def add_new_user_and_role(
        user_name_admin: Annotated[str, typer.Option(prompt=True)],
        password_admin: Annotated[str, typer.Option(prompt=True, hide_input=True)],

):
    controller: LoginController = ControllerFactory().create_object("login_controller")
    try:
        controller.login(user_name_admin, password_admin)
        print("logged_in")
        new_user_name = typer.prompt("Please add new username?")
        new_user_password = typer.prompt("password?", confirmation_prompt=True, hide_input=True)
        role = typer.prompt("role - ADMIN or NORMAL_USER")
        controller.add_new_user(new_user_name, new_user_password, role)
        print(new_user_name)
    except UserDeniedError as e:
        print(e.message)


@app.command()
def add_music_data(username: Annotated[str, typer.Option(prompt=True)],
                   password: Annotated[str, typer.Option(prompt=True, hide_input=True)]):
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
