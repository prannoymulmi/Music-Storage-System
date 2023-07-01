from src.controllers.login_controller import LoginController


def test_login():
    login = LoginController()
    result = login.login("some_user", "password")
    assert result == "logged in"

