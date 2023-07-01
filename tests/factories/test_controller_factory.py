from controllers.login_controller import LoginController
from src.factories.controller_factory import ControllerFactory


def test_create_object_when_login_controller_then_return_login_controller():
    cf = ControllerFactory()
    result = cf.create_object("login_controller")
    assert isinstance(result, LoginController)
