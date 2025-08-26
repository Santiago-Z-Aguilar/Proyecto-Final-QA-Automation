from API.utils.settings import AIRPORT
from API.tests.conftest import auth_headers
from API.utils.api_helpers import api_request
import faker
import pytest
import time

fake = faker.Faker()

@pytest.fixture
def airport(auth_headers):
    airport_data = {
        "iata_code": "PAZ",
        "city": "La Paz",
        "country": fake.country_code()
    }

    r = api_request("post", AIRPORT, json=airport_data, headers=auth_headers)

    if r.status_code != 201:
        print(f"[ERROR] No se pudo crear aeropuerto {airport_data['iata_code']}")
        print("Status:", r.status_code)
        print("Body:", r.text)

    r.raise_for_status()
    airport_response = r.json()

    yield airport_response
    for attempt in range(3):
        delete_r = api_request("delete", AIRPORT + f"/{airport_response['iata_code']}", headers=auth_headers)
        if delete_r.status_code in [200, 204]:
            break
        print(f"[WARN] Falló intento {attempt + 1} para eliminar aeropuerto. Status: {delete_r.status_code}")
        time.sleep(1)
    else:
        print(f"[ERROR] No se pudo eliminar aeropuerto después de 3 intentos.")

def test_airport(airport):
    print(airport)

