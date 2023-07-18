import typer
from sqlmodel import Session
from typing_extensions import Annotated

from configs.db_seeder import seed_database
from controllers.login_controller import LoginController
from controllers.music_data_controller import MusicDataController
from exceptions.data_not_found import DataNotFoundError
from exceptions.user_denied_exception import UserDeniedError
from exceptions.weak_password import WeakPasswordError
from factories.config_factory import ConfigFactory
from factories.controller_factory import ControllerFactory
from models.music_data import MusicData
from utils.general_utils import GeneralUtils
from utils.schema.token_input import TokenInput

app = typer.Typer()

session = None


@app.command()
def login(
        username: Annotated[
            str, typer.Option(prompt=True, callback=GeneralUtils.sanitize_user_name_and_password_input)],
        password: Annotated[str, typer.Option(prompt=True, hide_input=True,
                                              callback=GeneralUtils.sanitize_user_name_and_password_input)]
):
    controller: LoginController = ControllerFactory().create_object("login_controller")
    try:
        result = controller.login(username, password)
        if isinstance(result, TokenInput) and result:
            print("logged_in")
    except UserDeniedError as e:
        print(e.message)


@app.command()
def add_new_user_and_role(
        username_admin: Annotated[
            str, typer.Option(prompt=True, callback=GeneralUtils.sanitize_user_name_and_password_input)],
        password_admin: Annotated[
            str, typer.Option(prompt=True, hide_input=True,
                              callback=GeneralUtils.sanitize_user_name_and_password_input)],
        new_username: str = typer.Option("Please add new username?", prompt=True,
                                         callback=GeneralUtils.sanitize_user_name_and_password_input),
        new_user_password: str = typer.Option("password?", confirmation_prompt=True, hide_input=True,
                                              callback=GeneralUtils.sanitize_user_name_and_password_input),
        role: str = typer.Option("ROLE - ADMIN or NORMAL_USER", confirmation_prompt=True)
):
    controller: LoginController = ControllerFactory().create_object("login_controller")
    try:
        controller.login(username_admin, password_admin)
        print(f'logged_in as {username_admin}')
        controller.add_new_user(new_username, new_user_password, role)
        print(new_username)
    except UserDeniedError as e:
        print(e.message)
    except WeakPasswordError as e:
        print(e.message)


@app.command()
def add_music_data(
        username: Annotated[
            str, typer.Option(prompt=True, callback=GeneralUtils.sanitize_user_name_and_password_input)],
        password: Annotated[str, typer.Option(prompt=True, hide_input=True,
                                              callback=GeneralUtils.sanitize_user_name_and_password_input)],
        music_file_path: str = typer.Option(callback=GeneralUtils.sanitize_audio_file_input),
        music_score: int = typer.Option(callback=GeneralUtils.sanitize_int_input),
        lyrics_file_path: str = typer.Option()
):
    controller_login: LoginController = ControllerFactory().create_object("login_controller")
    controller_music: MusicDataController = ControllerFactory().create_object("music_controller")
    try:
        data: TokenInput = controller_login.login(username, password)
        controller_music.add_music_data(music_file_path, music_score, lyrics_file_path, data.user_data)
        print("data added")
    except UserDeniedError as e:
        print(e.message)


@app.command()
def update_music_data(
        username: str = typer.Option(default="", callback=GeneralUtils.sanitize_user_name_and_password_input),
        password: str = typer.Option(hide_input=True, default="",
                                     callback=GeneralUtils.sanitize_user_name_and_password_input),
        music_file_path: str = typer.Option(default="", callback=GeneralUtils.sanitize_audio_file_input),
        music_score: int = typer.Option(default=0, callback=GeneralUtils.sanitize_int_input),
        lyrics_file_path: str = typer.Option(default=""),
        music_data_id: int = typer.Option(callback=GeneralUtils.sanitize_int_input)
):
    controller_login: LoginController = ControllerFactory().create_object("login_controller")
    controller_music: MusicDataController = ControllerFactory().create_object("music_controller")
    try:
        login_data: TokenInput = controller_login.login(username, password)
        music_data = MusicData(
            id=music_data_id,
            music_file_name=music_file_path,
            music_score=music_score,
            lyrics_file_name=lyrics_file_path
        )
        controller_music.update_music_data(login_data.user_data, music_data)
        print("updated data")
    except UserDeniedError as e:
        print(e.message)
    except DataNotFoundError as e:
        print(e.message)


'''
This method only list the music data. If the user is an admin they can see all the user data, but a normal user
can only see their own data.
'''


@app.command()
def list_music_data(
        username: str = typer.Option(default="CHECK_TOKEN",
                                     callback=GeneralUtils.sanitize_user_name_and_password_input),
        password: str = typer.Option(hide_input=True, default="CHECK_TOKEN",
                                     callback=GeneralUtils.sanitize_user_name_and_password_input)
):
    controller_login: LoginController = ControllerFactory().create_object("login_controller")
    controller_music: MusicDataController = ControllerFactory().create_object("music_controller")
    try:
        data: TokenInput
        # If username and password are empty check if there is a valid token and get user details
        if username == "CHECK_TOKEN" and password == "CHECK_TOKEN":
            data = controller_login.get_details_for_token()
        else:
            data = controller_login.login(username, password)
        results = controller_music.list_music_data(data.user_data)
        print("Listing Data")
        for result in results:
            print(result)
    except UserDeniedError as e:
        print(e.message)
    except Exception as e:
        print(e.message)


@app.command()
def delete_music_data(
        username: str = typer.Option(callback=GeneralUtils.sanitize_user_name_and_password_input),
        password: str = typer.Option(hide_input=True, callback=GeneralUtils.sanitize_user_name_and_password_input),
        music_data_id: int = typer.Option(callback=GeneralUtils.sanitize_int_input)
):
    controller_login: LoginController = ControllerFactory().create_object("login_controller")
    controller_music: MusicDataController = ControllerFactory().create_object("music_controller")
    try:
        data: TokenInput = controller_login.login(username, password)
        controller_music.delete_music_data(data.user_data, music_data_id)
        print("Data Deleted")
    except UserDeniedError as e:
        print(e.message)


@app.command()
def download_music_data(
        username: str = typer.Option(callback=GeneralUtils.sanitize_user_name_and_password_input),
        password: str = typer.Option(hide_input=True, callback=GeneralUtils.sanitize_user_name_and_password_input),
        music_data_id: int = typer.Option(callback=GeneralUtils.sanitize_int_input)
):
    controller_login: LoginController = ControllerFactory().create_object("login_controller")
    controller_music: MusicDataController = ControllerFactory().create_object("music_controller")
    try:
        data: TokenInput = controller_login.login(username, password)
        music_data: MusicData = controller_music.get_music_data_by_id(data.user_data, music_data_id)
        print(
            f' ID: {music_data.id} Music Score:  {music_data.music_score} Music File: {music_data.music_file_name} Lyrics File: {music_data.lyrics_file_name}')
    except UserDeniedError as e:
        print(e.message)


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
