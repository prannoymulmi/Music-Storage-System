from unittest import mock

import utils.jwt_utils
from models.role import Role
from models.user import User
from src.utils.decorator_utils import encode_and_store_jwt
from utils.schema.token_input import TokenInput


@mock.patch.object(utils.jwt_utils.JWTUtils, "encode_jwt")
@mock.patch.object(utils.jwt_utils.JWTUtils, "store_jwt_in_config")
def test_when_encode_and_store_jwt_then_token_is_create_and_stored(mock_store_jwt, mock_encoder):
    mock_encoder.return_value = "test"

    @encode_and_store_jwt
    def to_be_decorated():
        return TokenInput(user_data=User(), role=Role())
    to_be_decorated()
    mock_encoder.assert_called_once()
    mock_store_jwt.assert_called_once()
    # mock_store_jwt.assert_not_called()
