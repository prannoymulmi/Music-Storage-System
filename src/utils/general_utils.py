import sys

import typer

MINIMUM_USER_PASS_VALUE = 5
MAX_USER_PASS_VALUE = 50


class GeneralUtils:
    @staticmethod
    def sanitize_user_name_and_password_input(value):
        if len(value) > MAX_USER_PASS_VALUE or len(value) < MINIMUM_USER_PASS_VALUE:
            raise typer.BadParameter(
                f'The minimum value should be {MINIMUM_USER_PASS_VALUE} and maximum should be {MAX_USER_PASS_VALUE}')
        return value

    @staticmethod
    def sanitize_int_input(value: int):
        if value > sys.maxsize or value < 0:
            raise typer.BadParameter(
                f'The minimum value should be {0} and maximum should be {sys.maxsize}')
        return value
