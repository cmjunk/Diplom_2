import allure


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user_success(self, api, registered_user):
        credentials = {
            "email": registered_user["data"]["email"],
            "password": registered_user["data"]["password"],
        }
        response = api.login_user(credentials)
        body = response.json()

        assert response.status_code == 200, "Код ответа должен быть 200"
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == credentials["email"]

    @allure.title("Логин с неверным логином и паролем")
    def test_login_with_invalid_credentials(self, api):
        credentials = {
            "email": "no_such_user_stellar@yandex.ru",
            "password": "wrong_password",
        }
        response = api.login_user(credentials)
        body = response.json()

        assert response.status_code == 401, "Код ответа должен быть 401"
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"
