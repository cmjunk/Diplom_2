import allure
import requests

from utils.endpoints import BASE_URL, REGISTER, LOGIN, LOGOUT, USER, ORDERS, INGREDIENTS

class StellarBurgersAPI:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    @staticmethod
    def _auth_headers(token: str) -> dict:
        return {"Authorization": token}

    # User

    @allure.step("Регистрация нового пользователя")
    def register_user(self, payload: dict) -> requests.Response:
        return requests.post(f"{self.base_url}{REGISTER}", json=payload)

    @allure.step("Логин пользователя")
    def login_user(self, payload: dict) -> requests.Response:
        return requests.post(f"{self.base_url}{LOGIN}", json=payload)

    @allure.step("Удаление пользователя")
    def delete_user(self, token: str) -> requests.Response:
        return requests.delete(f"{self.base_url}{USER}", headers=self._auth_headers(token))

    @allure.step("Логаут пользователя")
    def logout_user(self, refresh_token: str) -> requests.Response:
        return requests.post(f"{self.base_url}{LOGOUT}", json={"token": refresh_token})

    @allure.step("Получение данных пользователя")
    def get_user(self, token: str) -> requests.Response:
        return requests.get(f"{self.base_url}{USER}", headers=self._auth_headers(token))

    # Ingredients

    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self) -> requests.Response:
        return requests.get(f"{self.base_url}{INGREDIENTS}")

    # Orders

    @allure.step
    def create_order(self, payload: dict, token: str | None = None) -> requests.Response:
        headers = self._auth_headers(token) if token else {}
        return requests.post(f"{self.base_url}{ORDERS}", json=payload, headers=headers)