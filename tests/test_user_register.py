import allure
import pytest

from utils.data_generator import generate_user


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestUserRegister:

    @allure.title("Можно создать уникального пользователя")
    def test_create_unique_user_success(self, registered_user):
        response = registered_user["response"]
        body = response.json()

        assert response.status_code == 200, "Код ответа должен быть 200"
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == registered_user["data"]["email"]
        assert body["user"]["name"] == registered_user["data"]["name"]

    @allure.title("Нельзя создать пользователя, который уже зарегистрирован")
    def test_create_user_that_already_exists(self, api, registered_user):
        response = api.register_user(registered_user["data"])
        body = response.json()

        assert response.status_code == 403, "Код ответа должен быть 403"
        assert body["success"] is False
        assert body["message"] == "User already exists"

    @allure.title("Нельзя создать пользователя без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, api, missing_field):
        user_data = generate_user()
        del user_data[missing_field]

        response = api.register_user(user_data)
        body = response.json()

        assert response.status_code == 403, "Код ответа должен быть 403"
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"
