from auth.exceptions import TokenDecodeError
from auth.utils import decode_data_from_token
import pytest

from tests.utils import generate_random_string


async def test_decode_data_from_token():
    token = generate_random_string(100)
    with pytest.raises(TokenDecodeError):
        decode_data_from_token(token)
