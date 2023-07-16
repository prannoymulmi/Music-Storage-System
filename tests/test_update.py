from typer.testing import CliRunner

from main import app


def test_update():
    runner = CliRunner()
    result = runner.invoke(app,
                           ["update-music-data", "--username", "admin", "--password", "admin", "--lyrics-file-path ",
                            "tests/files/test2.txt", "--music-data-id", "1"])
    #result = runner.invoke(app, ['list-music-data', "--username", "test", "--password", "test"])