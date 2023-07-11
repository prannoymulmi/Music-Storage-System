import typer
from sqlmodel import Session
from typing_extensions import Annotated

from configs.db_seeder import seed_database
from controllers.login_controller import LoginController
from controllers.music_data_controller import MusicDataController
from exceptions.user_denied_exception import UserDeniedError
from exceptions.weak_password import WeakPasswordError
from factories.config_factory import ConfigFactory
from factories.controller_factory import ControllerFactory
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
    except WeakPasswordError as e:
        print(e.message)


@app.command()
def add_music_data(
        username: Annotated[str, typer.Option(prompt=True)],
        password: Annotated[str, typer.Option(prompt=True, hide_input=True)],
        music_file_path: str = typer.Option(),
        music_score: int = typer.Option(),
        lyrics_file_path: str = typer.Option()
):
    controller_login: LoginController = ControllerFactory().create_object("login_controller")
    controller_music: MusicDataController = ControllerFactory().create_object("music_controller")
    try:
        data: TokenInput = controller_login.login(username, password)
        print("logged_in")
        controller_music.add_music_data(music_file_path, music_score, lyrics_file_path, data.user_data)
    except UserDeniedError as e:
        print(e.message)


'''
This method only list the music data. If the user is an admin they can see all the user data, but a normal user
can only see their own data.
'''
@app.command()
def list_music_data(username: Annotated[str, typer.Option(prompt=True)],
                    password: Annotated[str, typer.Option(prompt=True, hide_input=True)]):
    controller_login: LoginController = ControllerFactory().create_object("login_controller")
    controller_music: MusicDataController = ControllerFactory().create_object("music_controller")
    try:
        data: TokenInput = controller_login.login(username, password)
        print("logged_in")
        results = controller_music.list_music_data(data.user_data)
        for result in results:
            print(result)
    except UserDeniedError as e:
        print(e.message)


@app.command()
def delete_music_data():
    print("deleting")


def load_app_config() -> Session:
    loader = ConfigFactory().create_object('config_loader')
    session_from_config = loader.load_config()
    seed_database(session_from_config)
    return session_from_config


def main():
    load_app_config()
    app()


if __name__ == "__main__":
    main()
