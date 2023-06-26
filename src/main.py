from pathlib import Path

import typer

from utils.configLoader import ConfigLoader

APP_NAME = "my-super-cli-app"

import click

app = typer.Typer()

@click.group()
def cli():
    main()
    pass

@click.command()
def login():
    click.echo("login")

@click.command()
def add_music_data():
    click.echo("Dropped the database")

@app.command()
def list_music_data():
    print("Typer is now below Click, the Click app is the top level")

def main():
    loader = ConfigLoader()
    loader.load_config()


typer_click_object = typer.main.get_command(app)
cli.add_command(typer_click_object, "list_music_data")
cli.add_command(login)
cli.add_command(add_music_data)

if __name__ == "__main__":
    cli()