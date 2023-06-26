from unittest import mock
from unittest.mock import MagicMock

from click.testing import CliRunner

from src.main import cli
from src.utils.configLoader import ConfigLoader


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ['login'])
    assert 'login' in result.output

@mock.patch("src.main.ConfigLoader.load_config")
def test_list_music_data(
        mock__ConfigLoader__load_config
):
    mock__ConfigLoader__load_config.return_value = None
    runner = CliRunner()
    result = runner.invoke(cli, ['list_music_data'])
    assert 'Typer is now below Click, the Click app is the top level' in result.output

def side_effect(arg):
    test = MagicMock(ConfigLoader())
    values = {'a': ConfigLoader(), 'b': 2, 'c': 3}

    test.load_config.return_value = "YOL"
    values = {'a': test, 'b': 2, 'c': 3}
    return values[arg]

@mock.patch("src.main.Creator.create_object")
def test_list_music_data_te(
        mock__creator
):
    test = MagicMock(ConfigLoader())
    values = {'a': ConfigLoader(), 'b': 2, 'c': 3}

    test.load_config.return_value = "YOL"
    mock__creator.side_effect= side_effect
    runner = CliRunner()
    result = runner.invoke(cli, ['list_music_data'])
    assert 'Typer is now below Click, the Click app is the top level' in result.output
