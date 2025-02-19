import pytest
from fastapi import status

from auth.enums import TokenTypesEnum
from auth.exceptions import TokenDoNotSet, NotValidTokenType
from auth.utils import create_token
from tests.utils import generate_random_string, generate_random_valid_password
from users.repositories import UserRepository

ENDPOINT_URL_MAPPER = {
    "list": "/api/image_folder/users/",
    "detail": "/api/image_folder/users/{}/",
    "create": "/api/image_folder/users/",
    "update": "/api/image_folder/users/{}/",
    "me": "/api/image_folder/users/me/",
    "delete": "/api/image_folder/users/",
    "reset_password": "/api/image_folder/users/{}/reset-password/",
    "set_password": "/api/image_folder/users/set-new-password/",
}


async def test_get_list_users(
    create_user,
    async_client,
    async_session,
):
    users_count = 0
    for _ in range(5):
        await create_user()
        users_count += 1
    user = await create_user(username="Vanko", firstname="Иван", lastname="Иванов")
    users_count += 1
    url = ENDPOINT_URL_MAPPER["list"]

    response = await async_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["meta"]["objects_count"] == users_count
    assert user.username in [user["username"] for user in response_data["items"]]


async def test_get_user_detail(
    create_user,
    async_client,
    async_session,
):
    user = await create_user(username="Vanko", firstname="Иван", lastname="Иванов")
    url = ENDPOINT_URL_MAPPER["detail"].format(str(user.id))

    response = await async_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(user.id)


async def test_create_user(
    async_client,
    async_session,
):
    password = generate_random_valid_password(5)
    data = {
        "username": generate_random_string(5),
        "firstname": generate_random_string(5),
        "lastname": generate_random_string(5),
        "email": generate_random_string(5) + "@mail.ru",
        "password": password,
        "confirm_password": password,
        "code_phrase": generate_random_string(5),
    }
    url = ENDPOINT_URL_MAPPER["create"]

    response = await async_client.post(url, json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == data["username"]
    assert response.json()["email"] == data["email"]


async def test_create_user_already_exists_username(create_user, async_client):
    username = generate_random_string(5)
    await create_user(username=username)

    password = generate_random_valid_password(5)
    data = {
        "username": username,
        "firstname": generate_random_string(5),
        "lastname": generate_random_string(5),
        "email": generate_random_string(5) + "@mail.ru",
        "password": password,
        "confirm_password": password,
        "code_phrase": generate_random_string(5),
    }

    url = ENDPOINT_URL_MAPPER["create"]
    response = await async_client.post(url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.json()["detail"] == f"Пользователь с именем {username} уже существует!"
    )


async def test_create_user_already_exists_email(create_user, async_client):
    email = generate_random_string(5) + "@mail.ru"
    await create_user(email=email)

    password = generate_random_valid_password(5)
    data = {
        "username": generate_random_string(5),
        "firstname": generate_random_string(5),
        "lastname": generate_random_string(5),
        "email": email,
        "password": password,
        "confirm_password": password,
        "code_phrase": generate_random_string(5),
    }

    url = ENDPOINT_URL_MAPPER["create"]
    response = await async_client.post(url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == f"Пользователь с email {email} уже существует!"


async def test_create_user_password_does_not_confirmed(
    async_client,
    async_session,
):
    data = {
        "username": generate_random_string(5),
        "firstname": generate_random_string(5),
        "lastname": generate_random_string(5),
        "email": generate_random_string(5) + "@mail.ru",
        "password": generate_random_string(5),
        "confirm_password": generate_random_string(5),
        "code_phrase": generate_random_string(5),
    }
    url = ENDPOINT_URL_MAPPER["create"]

    response = await async_client.post(url, json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_create_user_password_does_not_match_regex(
    async_client,
    async_session,
):
    data = {
        "username": generate_random_string(5),
        "firstname": generate_random_string(5),
        "lastname": generate_random_string(5),
        "email": generate_random_string(5) + "@mail.ru",
        "password": "qweqwe",
        "confirm_password": "qweqwe",
        "code_phrase": generate_random_string(5),
    }
    url = ENDPOINT_URL_MAPPER["create"]

    response = await async_client.post(url, json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_update_user(
    create_user,
    async_client,
    async_session,
):
    user = await create_user(
        username="Vanko", firstname="Иван", lastname="Иванов", email="ivan@mail.ru"
    )
    data = {"email": "ivan_vanko_ivanov@mail.ru"}
    url = ENDPOINT_URL_MAPPER["update"].format(str(user.id))

    response = await async_client.patch(url, json=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(user.id)
    assert response.json()["email"] == data["email"]


async def test_get_me(
    create_user,
    async_client,
    async_session,
):
    user_data = {"username": "Vanko"}
    user = await create_user(**user_data)
    access_token = create_token(TokenTypesEnum.access, user.username)
    url = ENDPOINT_URL_MAPPER["me"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await async_client.get(url, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user_data["username"]


async def test_get_me_user_not_found(
    async_client,
    async_session,
):
    access_token = create_token(TokenTypesEnum.access, generate_random_string(5))
    url = ENDPOINT_URL_MAPPER["me"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await async_client.get(url, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Пользователь не найден."


async def test_get_me_not_valid_token_no_bearer(
    async_client,
    async_session,
):
    access_token = create_token(TokenTypesEnum.access, generate_random_string(5))
    url = ENDPOINT_URL_MAPPER["me"]
    headers = {"Authorization": f"{access_token}"}

    with pytest.raises(NotValidTokenType):
        await async_client.get(url, headers=headers)


async def test_get_me_no_token(
    async_client,
    async_session,
):
    url = ENDPOINT_URL_MAPPER["me"]

    with pytest.raises(TokenDoNotSet):
        await async_client.get(url)


async def test_delete_user(
    create_user,
    async_client,
    async_session,
):
    user = await create_user()
    access_token = create_token(TokenTypesEnum.access, user.username)
    url = ENDPOINT_URL_MAPPER["delete"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await async_client.delete(url, headers=headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    repository = UserRepository(async_session)
    assert await repository.get_by_id(user.id) is None


@pytest.mark.parametrize(
    "password, valid_confirm_password, code_phrase, is_valid_code_phrase, expected_status_code, expected_response",
    [
        (
            generate_random_valid_password(5),
            True,
            generate_random_string(5),
            True,
            status.HTTP_200_OK,
            True,
        ),
        (
            generate_random_valid_password(5),
            False,
            generate_random_string(5),
            False,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            generate_random_valid_password(5),
            True,
            generate_random_string(5),
            False,
            status.HTTP_200_OK,
            False,
        ),
    ],
)
async def test_reset_password(
    password,
    valid_confirm_password,
    code_phrase,
    is_valid_code_phrase,
    expected_status_code,
    expected_response,
    create_user,
    async_client,
    async_session,
):
    data = {"password": password, "code_phrase": code_phrase}
    user = await create_user(**data)
    if valid_confirm_password:
        data["confirm_password"] = password
        data["code_phrase"] = code_phrase
    else:
        data["confirm_password"] = generate_random_valid_password(5)
        data["code_phrase"] = code_phrase
    if not is_valid_code_phrase:
        data["code_phrase"] = "qweqweewq"
    url = ENDPOINT_URL_MAPPER["reset_password"].format(str(user.id))

    response = await async_client.post(url, json=data)

    assert response.status_code == expected_status_code

    if is_valid_code_phrase:
        assert response.json() == expected_response


@pytest.mark.parametrize(
    "password, valid_confirm_password, expected_status_code",
    [
        (generate_random_valid_password(5), True, status.HTTP_200_OK),
        (
            generate_random_valid_password(5),
            False,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ],
)
async def test_set_new_password(
    password,
    valid_confirm_password,
    expected_status_code,
    create_user,
    async_client,
    async_session,
):
    data = {"password": password}
    user = await create_user(**data)
    if valid_confirm_password:
        data["confirm_password"] = password
    else:
        data["confirm_password"] = generate_random_valid_password(5)
    url = ENDPOINT_URL_MAPPER["set_password"]
    access_token = create_token(TokenTypesEnum.access, user.username)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await async_client.post(url, json=data, headers=headers)

    assert response.status_code == expected_status_code
