import typer
from sqlmodel import Session
from typing_extensions import Annotated

from controllers.login_controller import LoginController
from factories.config_factory import ConfigFactory
from factories.controller_factory import ControllerFactory
from utils.schema.token_input import TokenInput

app = typer.Typer()

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
def add_new_user_and_role(
        user_name_admin: Annotated[str, typer.Option(prompt=True)],
        password_admin: Annotated[str, typer.Option(prompt=True, hide_input=True)],

):
    controller: LoginController = ControllerFactory().create_object("login_controller")
    result = controller.login(user_name_admin, password_admin, load_app_config())
    if isinstance(result, TokenInput) and result.role.role_name == "ADMIN":
        print("logged_in")
        new_user_name = typer.prompt("Please add new username?", hide_input=True)
        new_user_password = typer.prompt("password?", confirmation_prompt=True, hide_input=True)
        controller.add_new_user(new_user_name, new_user_password)
        print(new_user_name)
    else:
        print("access_denied")


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
