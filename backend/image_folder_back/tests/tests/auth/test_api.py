from fastapi import status
from auth.enums import TokenTypesEnum
from auth.schemas import AuthTokenResponseSchema
from auth.utils import create_token, decode_data_from_token
from auth.hasher import Hasher


async def test_login(
    create_user,
    async_client,
    async_session,
):
    password = "qweqwe"
    user_data = {
        "username": "Vanko",
        "firstname": "Иван",
        "lastname": "Иванов",
        "password": Hasher.get_password_hash(password),
    }
    await create_user(**user_data)
    username = user_data["username"]
    data = {
        "username": username,
        "password": password,
    }
    url = "/api/image_folder/auth/token/"
    response = await async_client.post(url, json=data)
    assert response.status_code == status.HTTP_200_OK
    validated_data = AuthTokenResponseSchema(**response.json())
    assert decode_data_from_token(validated_data.access_token) == user_data["username"]
    assert (
        decode_data_from_token(validated_data.refresh_token, TokenTypesEnum.refresh)
        == user_data["username"]
    )


async def test_refresh(
    create_user,
    async_client,
    async_session,
):
    user_data = {
        "username": "Vanko",
        "firstname": "Иван",
        "lastname": "Иванов",
        "password": "qweqweqwe",
    }
    user = await create_user(**user_data)
    refresh = create_token(TokenTypesEnum.refresh, user.username)
    data = {
        "refresh_token": refresh,
    }
    url = "/api/image_folder/auth/refresh/"
    response = await async_client.post(url, json=data)
    assert response.status_code == status.HTTP_200_OK
    validated_data = AuthTokenResponseSchema(**response.json())
    assert (
        decode_data_from_token(validated_data.refresh_token, TokenTypesEnum.refresh)
        == user_data["username"]
    )
