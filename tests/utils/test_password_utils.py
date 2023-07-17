from pathlib import Path
from unittest.mock import MagicMock

import requests

from utils.password_utils import PasswordUtil

COMPLIANT_PASSWORD = "Amazing$GoodPassW0rd$4&?"
NON_COMPLIANT_PASSWORD = "test"

def test_check_is_password_compromised_password_in_have_i_been_pawned_when_breached_password_is_given_then_true_is_returned():
    with open(f"{Path(__file__).parent.parent}/utils/test_password_hashes.txt") as f:
        s = f.read()
        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = s
        requests.get.return_value = mock_response
        result = PasswordUtil.is_password_compromised_password_in_have_i_been_pawned(NON_COMPLIANT_PASSWORD)
        assert result


def test_is_password_compromised_password_in_have_i_been_pawned_when_non_breached_password_is_given_then_false_is_returned():
    with open(f"{Path(__file__).parent.parent}/utils/test_password_hashes.txt") as f:
        s = f.read()
        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = s
        requests.get.return_value = mock_response
        result = PasswordUtil.is_password_compromised_password_in_have_i_been_pawned((COMPLIANT_PASSWORD))
        assert not result

def test_is_password_policy_non_compliant_when_compliant_password_then_return_false():
    result = PasswordUtil.is_password_policy_non_compliant(COMPLIANT_PASSWORD)
    assert not result

def test_is_password_policy_non_compliant_when_non_compliant_password_then_return_true():
    result = PasswordUtil.is_password_policy_non_compliant(NON_COMPLIANT_PASSWORD)
    assert result

def test_is_password_policy_non_compliant_when_non_compliant_longer_than_30_password_then_return_true():
    result = PasswordUtil.is_password_policy_non_compliant("!FPSEwB^KMuzep6bK6@1rrPJZx!8T78S2v6J2aUNF1ZKKavpDf")
    assert result
