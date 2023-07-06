from datetime import timezone, timedelta, datetime
from unittest.mock import ANY
from unittest.mock import Mock

import pytest
from freezegun import freeze_time
from jwt.exceptions import JWTDecodeError
from jwt.utils import get_int_from_datetime

from utils.jwt_utils import encode_jwt, decode_jwt, instance
from utils.schema.TokenMessage import TokenMessage

"""
Using freeze time to mock date and time, 
so that the test always returns deterministic results
"""
@freeze_time("2023-06-8")
def test_encode_jwt_when_default_sub_then_encode_is_called_with_right_parameters():
    iat = datetime.now(timezone.utc)
    expected_message = TokenMessage(iss="music_storage_system",
                                    sub="",
                                    iat=get_int_from_datetime(iat),
                                    exp=get_int_from_datetime(
                                        iat + timedelta(minutes=5)))
    instance.encode = Mock()
    encode_jwt()
    instance.encode.assert_called_with(expected_message.dict(), ANY, alg='RS256')


def test_decode_jwt_when_correct_valid_token_then_returns_decoded_token():
    expected_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiAiYXNtaXMiLCAic3ViIjogIiIsICJpYXQiOiAxNjY4NzgxMzE5LCAiZXhwIjogNDgyMjM4MTMxOX0.edjsqikVLmOqzA_xt5phURKy9KkpCCEStziOUn7mvW7uJzRqpPX_74svoIaOqsKZuSd4evfGoyKRwkafUiKAsGwgRqrxbrfprtCVVUes1lgyD2DWq97f1Xyuwk1LSQrVrvhgmgwlJBj7py-xn03zyjSU8rnueRzadiqzNsEavdSDqGOmIfn1x4WmdKOny7tUSUxtTNyEBYq89wcDQcK2aUFSTyQXS7NZtc0hHK2P4jRj6mHu6qawQg8HpjByvZ5vkRyEr-M08O6Ro_-bMc52IRiXXEiyZuSZFJq6TxjXWwNkAHmNi_gtRhnQL295GaKE35MXVVatCxVWRYBdvH0tfw"
    res: TokenMessage = decode_jwt(expected_token)
    assert res is not None
    assert res['exp'] == 4822381319

def test_decode_jwt_when_spoofed_jwt_token_then_token_cannot_be_decoded_error_is_returned():
    spoofed_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiAiYXNtaXMiLCAic3ViIjogIiIsICJpYXQiOiAxNjY4Nzk1MjA0LCAiZXhwIjogMTY2ODc5NzAwNH0.Ps3vactKYLdTswW7zd-8msBofiICxmQHegIdIqNcmaw8DshmCN7TWrARJ8LKmx59jRO3g-MXTqwTYWJSOdMfJD13kV_uciv4ZBmHLzqq-e28Dup4RBQz9uc19rWhilK5fXbP5lpWF4IHukl_9_krDXfYADZPn9zXebxb6QRijkVPLLNnx4Vh_xIo_Yuahsz6X5cINmGrluIkE9G_csRSSPjbSNWwYzi4EE2Dqgi0iEKgkgnPyXCpgJb0YhKHbzmNFsniRZv3HhAZDRFlBiyG2pK0fpaHvD4ZAXu1PZU2RlCbTM4BamMiuNuQE2LqV4DwQU2V9pYFTL7avQ6Pyxp222P1HxZLw8hZe-yOndd60F5aXYY0bGa0GrhZivq1sfI4oUJcV6rtuCaj7HFOLGfGIgOrpMtoOu_P7gxKrOdLuHyUpE8XqeZScildJ5b_58_2lGrIFzeuA8yYlStWNJRr1hbg-PT3x9EEHEF4YboghG-izc07aSpGcn-c1cQQRzjdMEiAwHYX5uZ31b6EwSrRlptl-2gENb04pqE0ea58sHZFjKfKyAyNNfj1etyADWK0w4ziYT_HUuD2X6Kht4dRYV19xWCCKZ1frgsmsZOcZEeBdBMItOfaIPdaFGvGe6mdvRwdmSdFhtDeZuQpxlCLt6rDF6kmGC8Yu5_QmJ3wgK4"
    with pytest.raises(JWTDecodeError):
        decode_jwt(spoofed_token)
