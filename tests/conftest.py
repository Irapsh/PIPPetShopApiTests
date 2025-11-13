import requests
import pytest

BASE_URL = 'http://5.181.109.28:9090/api/v3'

@pytest.fixture(scope="function")
#Фикстура для создания питомца
def create_pet():
    payload = {
        "id": 11,
        "name": "Buddy",
        "status": "available"
    }

    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    return response.json()

@pytest.fixture(scope="function")
#Фикстура для создания заказа
def create_order():
    payload = {
        "id": 1,
        "petId": 1,
        "quantity": 1,
        "status": "placed",
        "complete": True
    }

    response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
    return response.json()