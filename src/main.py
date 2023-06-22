from pathlib import Path

import typer

from utils.ConfigLoader import ConfigLoader

APP_NAME = "my-super-cli-app"

import click


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

@click.command()
def list_music_data():
    click.echo("listed music")

def main():
    loader = ConfigLoader()
    loader.load_config()


cli.add_command(login)
cli.add_command(add_music_data)
cli.add_command(list_music_data)

if __name__ == "__main__":
    cli()