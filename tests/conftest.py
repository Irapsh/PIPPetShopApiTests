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
