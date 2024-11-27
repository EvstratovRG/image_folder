from fastapi import status

from auth.enums import TokenTypesEnum
from auth.utils import create_token
from tests.utils import generate_random_string

ENDPOINT_URL_MAPPER = {
    "list": "/api/image_folder/users/",
    "detail": "/api/image_folder/users/{}/",
    "create": "/api/image_folder/users/",
    "update": "/api/image_folder/users/{}/",
    "me": "/api/image_folder/users/me/",
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
    url = ENDPOINT_URL_MAPPER.get("list")
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
    url = ENDPOINT_URL_MAPPER.get("detail").format(str(user.id))
    response = await async_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(user.id)


async def test_create_user(
    async_client,
    async_session,
):
    data = {
        "username": generate_random_string(5),
        "firstname": generate_random_string(5),
        "lastname": generate_random_string(5),
        "email": generate_random_string(5) + "@mail.ru",
        "password": generate_random_string(5),
        "code_phrase": generate_random_string(5),
    }
    url = ENDPOINT_URL_MAPPER.get("create")
    response = await async_client.post(url, json=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == data["username"]
    assert response.json()["email"] == data["email"]


async def test_update_user(
    create_user,
    async_client,
    async_session,
):
    user = await create_user(
        username="Vanko", firstname="Иван", lastname="Иванов", email="ivan@mail.ru"
    )
    data = {"email": "ivan_vanko_ivanov@mail.ru"}
    url = ENDPOINT_URL_MAPPER.get("update").format(str(user.id))
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
    url = ENDPOINT_URL_MAPPER.get("me")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await async_client.get(url, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == user_data["username"]
