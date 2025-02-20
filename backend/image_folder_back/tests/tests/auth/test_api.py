from fastapi import status
from auth.enums import TokenTypesEnum
from auth.schemas import AuthTokenResponseSchema
from auth.utils import create_token, decode_data_from_token
from tests.utils import generate_random_valid_password, generate_random_string


async def test_login(
    create_user,
    async_client,
    async_session,
):
    password = generate_random_valid_password(5)
    user_data = {
        "username": "Vanko",
        "firstname": "Иван",
        "lastname": "Иванов",
        "password": password,
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


async def test_login_user_not_found(
    async_client,
    async_session,
):
    username = generate_random_string(5)
    data = {
        "username": username,
        "password": generate_random_valid_password(5),
    }
    url = "/api/image_folder/auth/token/"

    response = await async_client.post(url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == f"Пользователь {username} не найден."


async def test_login_password_does_not_match(
    create_user,
    async_client,
    async_session,
):
    user_data = {
        "username": "Vanko",
        "firstname": "Иван",
        "lastname": "Иванов",
        "password": generate_random_valid_password(5),
    }
    await create_user(**user_data)
    username = user_data["username"]
    data = {
        "username": username,
        "password": generate_random_valid_password(5),
    }
    url = "/api/image_folder/auth/token/"

    response = await async_client.post(url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Не верный пароль."


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


async def test_refresh_user_not_found(
    async_client,
    async_session,
):
    refresh = create_token(TokenTypesEnum.refresh, generate_random_string())
    data = {
        "refresh_token": refresh,
    }
    url = "/api/image_folder/auth/refresh/"

    response = await async_client.post(url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Пользователь по токену - не найден."
