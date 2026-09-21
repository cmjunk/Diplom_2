import allure
import pytest

@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestOrderCreate:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth(self, api, registered_user, ingredient_ids):
        payload = {"ingredients": ingredient_ids}
        response = api.create_order(payload, token=registered_user["accessToken"])
        body = response.json()

        assert response.status_code == 200, "Код ответа должен быть 200"
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, api, ingredient_ids):
        payload = {"ingredients": ingredient_ids}
        response = api.create_order(payload)
        body = response.json()

        assert response.status_code == 200, "Код ответа должен быть 200"
        assert body["success"] is True
        assert "order" in body

    @allure.title("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self, api, registered_user, ingredient_ids):
        payload = {"ingredients": ingredient_ids}
        response = api.create_order(payload, token=registered_user["accessToken"])
        body = response.json()

        assert response.status_code == 200, "Код ответа должен быть 200"
        assert body["success"] is True
        assert len(body["order"]["ingredients"]) == len(ingredient_ids)

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, api, registered_user):
        payload = {"ingredients": []}
        response = api.create_order(payload, token=registered_user["accessToken"])
        body = response.json()

        assert response.status_code == 400, "Код ответа должен быть 400"
        assert body["success"] is False
        assert body["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, api, registered_user):
        payload = {"ingredients": ["invalid_hash_123"]}
        response = api.create_order(payload, token=registered_user["accessToken"])

        assert response.status_code == 500, "Код ответа должен быть 500"
  