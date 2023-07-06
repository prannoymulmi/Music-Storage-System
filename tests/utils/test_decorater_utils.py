from unittest import mock

import utils.jwt_utils
from src.utils.decorator_utils import encode_and_store_jwt


@mock.patch.object(utils.jwt_utils.JWTUtils, "encode_jwt")
@mock.patch.object(utils.jwt_utils.JWTUtils, "store_jwt_in_config")
def test_should_select_outgoing_address_for_managers(mock_store_jwt, mock_encoder):
    mock_encoder.return_value = "test"

    @encode_and_store_jwt
    def to_be_decorated():
        return "logged in"
    to_be_decorated()
    mock_encoder.assert_called_once()
    mock_store_jwt.assert_called_once()
    #mock_store_jwt.assert_not_called()