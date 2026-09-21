import pytest

from utils.api_client import StellarBurgersAPI
from utils.data_generator import generate_user


@pytest.fixture
def api() -> StellarBurgersAPI:
    return StellarBurgersAPI()


@pytest.fixture
def registered_user(api):
    """
    Создаёт нового пользователя перед тестом и гарантированно удаляет его после,
    чтобы тесты не оставляли мусор в базе и не мешали друг другу.
    """
    user_data = generate_user()
    response = api.register_user(user_data)
    body = response.json()

    user = {
        "data": user_data,
        "response": response,
        "accessToken": body.get("accessToken"),
        "refreshToken": body.get("refreshToken"),
    }

    yield user

    token = user.get("accessToken")
    if token:
        api.delete_user(token)

@pytest.fixture
def ingredient_ids(api):
    response = api.get_ingredients()
    data = response.json()["data"]
    return [data[0]["_id"], data[1]["_id"]]
