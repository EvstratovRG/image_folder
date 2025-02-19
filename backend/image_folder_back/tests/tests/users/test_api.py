import pytest
from fastapi import status

from auth.enums import TokenTypesEnum
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
    "restore_password": "/api/image_folder/users/{}/restore-password/",
    "set_password": "/api/image_folder/users/{}/set-new-password/",
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
    assert len(response_data) == users_count
    assert user.username in [user["username"] for user in response_data]


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
    "code_phrase, is_valid, expected_response",
    [
        (generate_random_string(5), True, True),
        (generate_random_string(5), False, False),
    ],
)
async def test_restore_password(
    code_phrase,
    is_valid,
    expected_response,
    create_user,
    async_client,
    async_session,
):
    data = {}
    if is_valid:
        data["code_phrase"] = code_phrase
    user = await create_user(**data)
    if not is_valid:
        data["code_phrase"] = "qweqwe"
    url = ENDPOINT_URL_MAPPER["restore_password"].format(str(user.id))

    response = await async_client.post(url, json=data)

    assert response.status_code == status.HTTP_200_OK
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
    url = ENDPOINT_URL_MAPPER["set_password"].format(str(user.id))

    response = await async_client.post(url, json=data)

    assert response.status_code == expected_status_code
