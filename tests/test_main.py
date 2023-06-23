from unittest import mock

import pytest
from click.testing import CliRunner

from src.main import cli
from src.utils.ConfigLoader import ConfigLoader

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
