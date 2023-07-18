import sys

import pytest
import typer

from utils.general_utils import GeneralUtils

MINIMUM_USER_PASS_VALUE = 5
MAX_USER_PASS_VALUE = 50


def test_sanitize_user_name_and_password_input_with_correct_value_then_string_is_returned():
    valid_string = "username1"
    result = GeneralUtils.sanitize_user_name_and_password_input(valid_string)
    assert result == valid_string


def test_sanitize_user_name_and_password_input_with_long_value_then_typer_error_is_returned():
    invalid_string = "VeryVeryLongTextVeryVeryLongTextVeryVeryLongTextVeryVeryLongTextVeryVeryLongTextVeryVeryLongTextVeryVeryLongText"
    with pytest.raises(typer.BadParameter,
                       match=f'The minimum value should be {MINIMUM_USER_PASS_VALUE} and maximum should be {MAX_USER_PASS_VALUE}'):
        GeneralUtils.sanitize_user_name_and_password_input(invalid_string)


def test_sanitize_int_input_with_correct_value_then_string_is_returned():
    valid_int = 500000
    result = GeneralUtils.sanitize_int_input(valid_int)
    assert result == valid_int


def test_sanitize_int_input_with_long_value_then_typer_error_is_returned():
    invalid_int = sys.maxsize + 1
    with pytest.raises(typer.BadParameter,
                       match=f'The minimum value should be {0} and maximum should be {sys.maxsize}'):
        GeneralUtils.sanitize_int_input(invalid_int)
