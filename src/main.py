import typer
from rich import print
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
from utils.schema.music_data_output import MusicDataOutput
from utils.general_utils import GeneralUtils
from utils.schema.token_input import TokenInput

# Do not show exception data in the console
app = typer.Typer(pretty_exceptions_enable=False)

"""
The entry point to the CLI application, it uses Typer to make to empower the CLI app.
"""

"""
The method which handles the login of users with all the other input sanitization step.
This method will create a signed JWT token stored encrypted in the local machine. This token
can be used to only list the data for users without re authentication, given the token is valid.
"""
@app.command()
def login(
        username: Annotated[
            str, typer.Option(prompt=True, callback=GeneralUtils.sanitize_user_name_and_password_input)],
        password: Annotated[str, typer.Option(prompt=True, hide_input=True,
                                              callback=GeneralUtils.sanitize_user_name_and_password_input)]
):
    # Using Factory pattern to create controller instances
    controller: LoginController = ControllerFactory().create_object("login_controller")
    try:
        result = controller.login(username, password)
        if isinstance(result, TokenInput) and result:
            print("[bold green]logged_in[bold green]")
    except UserDeniedError as e:
        print(f'[bold red]{e.message}[bold red]')
    except Exception as e:
        print(f'[bold red]{e.message}[bold red]')


"""
The method which handles adding new user with roles with all the other input sanitization step and authorization and authentication
process required for this action.
It is to be noted that only Admins are allowed to perform this operation.
"""
@app.command()
def add_new_user_and_role(
        username_admin: Annotated[
            str, typer.Option(
                prompt=True,
                callback=GeneralUtils.sanitize_user_name_and_password_input
            )],
        password_admin: Annotated[
            str, typer.Option(
                prompt=True,
                hide_input=True,
                callback=GeneralUtils.sanitize_user_name_and_password_input
            )],
        new_username: str = typer.Option(
            "Please add new username?",
            prompt=True,
            callback=GeneralUtils.sanitize_user_name_and_password_input
        ),
        new_user_password: str = typer.Option(
            "password?",
            confirmation_prompt=True,
            hide_input=True,
            callback=GeneralUtils.sanitize_user_name_and_password_input
        ),
        role: str = typer.Option("ROLE - ADMIN or NORMAL_USER", confirmation_prompt=True)
):
    # Using Factory pattern to create controller instances
    controller: LoginController = ControllerFactory().create_object("login_controller")
    try:
        controller.login(username_admin, password_admin)
        print(f'[bold green]logged_in as {username_admin}[bold green]')
        controller.add_new_user(new_username, new_user_password, role)
        print(f'[bold green] added new user : {new_username}[bold green]')
    except UserDeniedError as e:
        print(f'[bold red]{e.message}[bold red]')
    except WeakPasswordError as e:
        print(f'[bold red]{e.message}[bold red]')
    except Exception as e:
        print(f'[bold red]{e.message}[bold red]')

"""
The method which handles the adding new data with all the other input sanitization step and authorization and authentication
process required for this action.
"""
@app.command()
def add_music_data(
        username: Annotated[
            str, typer.Option(prompt=True, callback=GeneralUtils.sanitize_user_name_and_password_input)],
        password: Annotated[str, typer.Option(prompt=True, hide_input=True,
                                              callback=GeneralUtils.sanitize_user_name_and_password_input)],
        music_file_path: str = typer.Option(callback=GeneralUtils.sanitize_music_file_input),
        music_score: int = typer.Option(callback=GeneralUtils.sanitize_int_input),
        lyrics_file_path: str = typer.Option(callback=GeneralUtils.sanitize_lyrics_file_input)
):
    # Using Factory pattern to create controller instances
    controller_login: LoginController = ControllerFactory().create_object("login_controller")
    controller_music: MusicDataController = ControllerFactory().create_object("music_controller")
    try:
        data: TokenInput = controller_login.login(username, password)
        controller_music.add_music_data(music_file_path, music_score, lyrics_file_path, data.user_data)
        print("[bold green]data added[bold green]")
    except UserDeniedError as e:
        print(f'[bold red]{e.message}[bold red]')
    except Exception as e:
        print(f'[bold red]{e.message}[bold red]')

"""
The method which handles the update data with all the other input sanitization step and authorization and authentication
process required for this action.
"""
@app.command()
def update_music_data(
        username: str = typer.Option(default="", callback=GeneralUtils.sanitize_user_name_and_password_input),
        password: str = typer.Option(hide_input=True, default="",
                                     callback=GeneralUtils.sanitize_user_name_and_password_input),
        music_file_path: str = typer.Option(default="EMPTY", callback=GeneralUtils.sanitize_music_file_input),
        music_score: int = typer.Option(default=0, callback=GeneralUtils.sanitize_int_input),
        lyrics_file_path: str = typer.Option(default="EMPTY", callback=GeneralUtils.sanitize_lyrics_file_input),
        music_data_id: int = typer.Option(callback=GeneralUtils.sanitize_int_input)
):
    # Using Factory pattern to create controller instances
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
        print("[bold green]updated data[bold green]")
    except UserDeniedError as e:
        print(f'[bold red]{e.message}[bold red]')
    except DataNotFoundError as e:
        print(f'[bold red]{e.message}[bold red]')
    except Exception as e:
        print(f'[bold red]{e.message}[bold red]')

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
    # Using Factory pattern to create controller instances
    controller_login: LoginController = ControllerFactory().create_object("login_controller")
    controller_music: MusicDataController = ControllerFactory().create_object("music_controller")
    try:
        data: TokenInput
        """If username and password are default value (non input provided), then check 
        if there is a valid token and get user details"""
        if username == "CHECK_TOKEN" and password == "CHECK_TOKEN":  # nosec
            data = controller_login.get_details_for_token()
        else:
            data = controller_login.login(username, password)
        results: MusicDataOutput = controller_music.list_music_data(data.user_data)
        print("[bold green]Listing Data[bold green]")
        for result in results:
            print(f' id: {result.id} music_score: {result.music_score}'
                  f'music_file_name: {result.music_file_name} '
                  f'lyrics_file_name: {result.lyrics_file_name} '
                  f'checksum: {result.checksum} user_id: {result.user_id}'
                  f' modified_timestamp: {result.modified_timestamp} '
                  f'created_timestamp: {result.created_timestamp}')
    except UserDeniedError as e:
        print(f'[bold red]{e.message}[bold red]')
    except Exception as e:
        print(f'[bold red]{e.message}[bold red]')


"""
The method which handles the delete the data with all the other input sanitization step and authorization and authentication
process required for this action.
"""
@app.command()
def delete_music_data(
        username: str = typer.Option(callback=GeneralUtils.sanitize_user_name_and_password_input),
        password: str = typer.Option(hide_input=True, callback=GeneralUtils.sanitize_user_name_and_password_input),
        music_data_id: int = typer.Option(callback=GeneralUtils.sanitize_int_input)
):
    # Using Factory pattern to create controller instances
    controller_login: LoginController = ControllerFactory().create_object("login_controller")
    controller_music: MusicDataController = ControllerFactory().create_object("music_controller")
    try:
        data: TokenInput = controller_login.login(username, password)
        controller_music.delete_music_data(data.user_data, music_data_id)
        print("[bold red]Data Deleted[bold red]")
    except UserDeniedError as e:
        print(f'[bold red]{e.message}[bold red]')
    except Exception as e:
        print(f'[bold red]{e.message}[bold red]')

"""
The method which handles the download data with all the other input sanitization step and authorization and authentication
process required for this action.
"""
@app.command()
def download_music_data(
        username: str = typer.Option(callback=GeneralUtils.sanitize_user_name_and_password_input),
        password: str = typer.Option(hide_input=True, callback=GeneralUtils.sanitize_user_name_and_password_input),
        music_data_id: int = typer.Option(callback=GeneralUtils.sanitize_int_input)
):
    # Using Factory pattern to create controller instances
    controller_login: LoginController = ControllerFactory().create_object("login_controller")
    controller_music: MusicDataController = ControllerFactory().create_object("music_controller")
    try:
        data: TokenInput = controller_login.login(username, password)
        music_data: MusicData = controller_music.get_music_data_by_id(data.user_data, music_data_id)
        print(
            f' ID: {music_data.id} Music Score:  {music_data.music_score} Music File: {music_data.music_file_name} Lyrics File: {music_data.lyrics_file_name}')
    except UserDeniedError as e:
        print(f'[bold red]{e.message}[bold red]')
    except Exception as e:
        print(f'[bold red]{e.message}[bold red]')


"""
This Command initializes the application with the required admin roles and an admin user name and random password.
"""
@app.command()
def init():
    load_app_config(True)


"""
The method that loads all the configurations that the application needs to start. 
"""
def load_app_config(is_init: bool = False) -> Session:
    loader = ConfigFactory().create_object('config_loader')
    session_from_config = loader.load_config()
    if is_init:
        result = seed_database(session_from_config)
        if not result:
            print("[bold red] Application is already initialized ![bold red]")
    return session_from_config


def main():
    load_app_config()
    app()


if __name__ == "__main__":
    main()
