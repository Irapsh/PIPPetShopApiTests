import allure
import requests
import pytest
import jsonschema
from .schemas.store_schema import STORE_SCHEMA
from .schemas.inventory_schema import INVENTORY_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'

@allure.feature('Store')
class TestStore:
    @allure.title("Размещение заказа")
    def test_add_store(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with (allure.step("Проверка статуса ответа")):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка данных созданного заказа"):
            jsonschema.validate(response_json, STORE_SCHEMA)
            assert response_json["id"] == payload["id"], "Id заказа не совпадает с ожидаемым"
            assert response_json["petId"] == payload["petId"], "pet_id не совпадает с ожидаемым"
            assert response_json["quantity"] == payload["quantity"], "Количество не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "Статус не совпадает с ожидаемым"
            assert response_json["complete"] == payload["complete"], "Статус выполнения не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        with allure.step("Получение id созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о питомце по Id"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка данных созданного заказа"):
            jsonschema.validate(response_json, STORE_SCHEMA)
            assert response_json["id"] == order_id, "Id питомца не совпадает с ожидаемым"
            assert response_json["petId"] == create_order["petId"], "Имя питомца не совпадает с ожидаемым"
            assert response_json["quantity"] == create_order["quantity"], "Количество питомца не совпадает с ожидаемым"
            assert response_json["status"] == create_order["status"], "Статус не совпадает с ожидаемым"
            assert response_json["complete"] == create_order["complete"], "Статус выполнения не совпадает с ожидаемым"

    @allure.title("Удаление заказа по id")
    def test_delete_order_by_id(self, create_order):
        with (allure.step("Получение id созданного заказа")):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа по Id"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with (allure.step("Проверка статуса ответа")):
            assert response.status_code == 200, "Код ответа при удалении не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации о удалённом заказе по Id"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with (allure.step("Проверка статуса ответа")):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_getinfo_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with (allure.step("Проверка статуса ответа")):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with (allure.step(f"Получение инвентаря магазина")):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()

        with (allure.step("Проверка статуса ответа и формата данных")):
            jsonschema.validate(response_json, INVENTORY_SCHEMA)
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

