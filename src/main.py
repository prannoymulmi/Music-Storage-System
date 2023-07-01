import typer

from factory import Creator

APP_NAME = "music-storage-system"

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
    loader = Creator().create_object('a')
    print(loader.load_config())


typer_click_object = typer.main.get_command(app)
cli.add_command(typer_click_object, "list_music_data")
cli.add_command(login)
cli.add_command(add_music_data)

if __name__ == "__main__":
    cli()