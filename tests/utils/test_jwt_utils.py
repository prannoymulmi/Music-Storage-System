from datetime import timezone, timedelta, datetime
from unittest.mock import ANY
from unittest.mock import Mock

import pytest
from freezegun import freeze_time
from jwt.exceptions import JWTDecodeError
from jwt.utils import get_int_from_datetime

from models.role import Role
from models.user import User
from utils.jwt_utils import JWTUtils
from utils.schema.token import Token
from utils.schema.token_input import TokenInput

"""
Using freeze time to mock date and time, 
so that the test always returns deterministic results
"""
@freeze_time("2023-06-8")
def test_encode_jwt_when_default_sub_then_encode_is_called_with_right_parameters():
    iat = datetime.now(timezone.utc)
    expected_message = Token(iss="music_storage_system",
                             sub="1",
                             permissions=["test"],
                             user_id="1",
                             iat=get_int_from_datetime(iat),
                             exp=get_int_from_datetime(
                                        iat + timedelta(minutes=5)))

    JWTUtils.instance.encode = Mock()
    JWTUtils.encode_jwt(TokenInput(user_data=User(id=1),
                                   role=Role(
                                       id=1,
                                       role_name="test"
                                   )
                                   ))
    JWTUtils.instance.encode.assert_called_with(expected_message.dict(), ANY, alg='RS256')


def test_decode_jwt_when_correct_valid_token_then_returns_decoded_token():
    expected_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiAiYXNtaXMiLCAic3ViIjogIiIsICJpYXQiOiAxNjY4NzgxMzE5LCAiZXhwIjogNDgyMjM4MTMxOX0.edjsqikVLmOqzA_xt5phURKy9KkpCCEStziOUn7mvW7uJzRqpPX_74svoIaOqsKZuSd4evfGoyKRwkafUiKAsGwgRqrxbrfprtCVVUes1lgyD2DWq97f1Xyuwk1LSQrVrvhgmgwlJBj7py-xn03zyjSU8rnueRzadiqzNsEavdSDqGOmIfn1x4WmdKOny7tUSUxtTNyEBYq89wcDQcK2aUFSTyQXS7NZtc0hHK2P4jRj6mHu6qawQg8HpjByvZ5vkRyEr-M08O6Ro_-bMc52IRiXXEiyZuSZFJq6TxjXWwNkAHmNi_gtRhnQL295GaKE35MXVVatCxVWRYBdvH0tfw"
    res: Token = JWTUtils.decode_jwt(expected_token)
    assert res is not None
    assert res['exp'] == 4822381319

def test_decode_jwt_when_spoofed_jwt_token_then_token_cannot_be_decoded_error_is_returned():
    spoofed_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiAiYXNtaXMiLCAic3ViIjogIiIsICJpYXQiOiAxNjY4Nzk1MjA0LCAiZXhwIjogMTY2ODc5NzAwNH0.Ps3vactKYLdTswW7zd-8msBofiICxmQHegIdIqNcmaw8DshmCN7TWrARJ8LKmx59jRO3g-MXTqwTYWJSOdMfJD13kV_uciv4ZBmHLzqq-e28Dup4RBQz9uc19rWhilK5fXbP5lpWF4IHukl_9_krDXfYADZPn9zXebxb6QRijkVPLLNnx4Vh_xIo_Yuahsz6X5cINmGrluIkE9G_csRSSPjbSNWwYzi4EE2Dqgi0iEKgkgnPyXCpgJb0YhKHbzmNFsniRZv3HhAZDRFlBiyG2pK0fpaHvD4ZAXu1PZU2RlCbTM4BamMiuNuQE2LqV4DwQU2V9pYFTL7avQ6Pyxp222P1HxZLw8hZe-yOndd60F5aXYY0bGa0GrhZivq1sfI4oUJcV6rtuCaj7HFOLGfGIgOrpMtoOu_P7gxKrOdLuHyUpE8XqeZScildJ5b_58_2lGrIFzeuA8yYlStWNJRr1hbg-PT3x9EEHEF4YboghG-izc07aSpGcn-c1cQQRzjdMEiAwHYX5uZ31b6EwSrRlptl-2gENb04pqE0ea58sHZFjKfKyAyNNfj1etyADWK0w4ziYT_HUuD2X6Kht4dRYV19xWCCKZ1frgsmsZOcZEeBdBMItOfaIPdaFGvGe6mdvRwdmSdFhtDeZuQpxlCLt6rDF6kmGC8Yu5_QmJ3wgK4"
    with pytest.raises(JWTDecodeError):
        JWTUtils.decode_jwt(spoofed_token)
