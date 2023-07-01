from unittest import mock
from unittest.mock import MagicMock

from click.testing import CliRunner

from src.main import cli
from src.utils.configLoader import ConfigLoader


# @mock.patch("src.main.ConfigLoader.load_config")
# def test_list_music_data(
#         mock__ConfigLoader__load_config
# ):
#     mock__ConfigLoader__load_config.return_value = None
#     runner = CliRunner()
#     result = runner.invoke(cli, ['list-music-data'])
#     assert 'listing' in result.output

def side_effect(arg):
    test = MagicMock(ConfigLoader())
    values = {'config_loader': ConfigLoader(), 'b': 2, 'c': 3}

    test.load_config.return_value = "YOL"
    values = {'config_loader': test, 'b': 2, 'c': 3}
    return values[arg]

@mock.patch("src.main.Creator.create_object")
def test_when_list_music_data_then_is_listed(
        mock__creator
):
    test = MagicMock(ConfigLoader())
    values = {'config_loader': ConfigLoader(), 'b': 2, 'c': 3}

    test.load_config.return_value = "YOL"
    mock__creator.side_effect = side_effect
    runner = CliRunner()
    result = runner.invoke(cli, ['list-music-data'])
    assert 'Listing' in result.output

@mock.patch("src.main.Creator.create_object")
def test_when_login_with_right_credentials_then_user_is_logged_on(
        mock__creator
):
    test = MagicMock(ConfigLoader())

    test.load_config.return_value = "YOL"
    mock__creator.side_effect = side_effect
    runner = CliRunner()
    result = runner.invoke(cli, ['login'])
    assert 'login' in result.output