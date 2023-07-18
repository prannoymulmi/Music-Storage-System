from unittest import mock

from controllers.login_controller import LoginController
from controllers.music_data_controller import MusicDataController
from src.factories.controller_factory import ControllerFactory
from utils import configLoader


@mock.patch.object(configLoader.ConfigLoader, "load_config")
def test_create_object_when_login_controller_then_return_login_controller(mock):
    cf = ControllerFactory()
    result = cf.create_object("login_controller")
    assert isinstance(result, LoginController)


def test_create_object_when_unknown_then_return_none():
    cf = ControllerFactory()
    result = cf.create_object("unknown")
    assert result is None


@mock.patch.object(configLoader.ConfigLoader, "load_config")
def test_create_object_when_music_data_controller_then_return_music_data_controller(mock):
    cf = ControllerFactory()
    result = cf.create_object("music_controller")
    assert isinstance(result, MusicDataController)
