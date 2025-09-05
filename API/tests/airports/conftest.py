from API.tests.conftest import auth_headers
from API.utils.api_helpers import api_request
from API.utils.data import valid_iata_code, valid_city, valid_country
from API.utils.settings import AIRPORTS
import pytest,string,random

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

    r = api_request("post", AIRPORTS, json=airport_data, headers=auth_headers)

    if r.status_code != 201:
        print(f"[ERROR] No se pudo crear aeropuerto {airport_data['iata_code']}")
        print("Status:", r.status_code)
        print("Body:", r.text)

    r.raise_for_status()
    airport_response = r.json()

    yield airport_response
    for attempt in range(3):
        delete_r = api_request("delete", AIRPORTS + f"/{airport_response['iata_code']}", headers=auth_headers)
        if delete_r.status_code in [200, 204]:
            break
        print(f"[WARN] Falló intento {attempt + 1} para eliminar aeropuerto. Status: {delete_r.status_code}")
        time.sleep(1)
    else:
        print(f"[ERROR] No se pudo eliminar aeropuerto después de 3 intentos.")

def test_airport(airport):
    print(airport)

#=======================================
def _valid_airports():
    return {"iata_code": valid_iata_code, "city": valid_city, "country": valid_country}

def _populate(airports_needed,create_valid_airports):
    for i in range(0,airports_needed):
        create_valid_airports()

@pytest.fixture
def get_airport2(auth_headers):
    def _get_airport(case):
        iata_code = case.get("iata_code", valid_iata_code)
        response = api_request("get",f"{AIRPORTS}/{iata_code}", headers=auth_headers)
        return response
    return _get_airport

@pytest.fixture
def get_airport(auth_headers):
    def _get_airport(case):
        iata_code = case.get("iata_code", valid_iata_code)
        # Construir URL completa para debug
        url = f"{AIRPORTS}/{iata_code}"
        print("[DEBUG] GET con IATA_CODE URL:", url)  # <-- imprime la URL que se va a llamar
        response = api_request("get", url, headers=auth_headers)
        return response
    return _get_airport

def _random_iata_code():
    return ''.join(random.choices(string.ascii_uppercase, k=3))

@pytest.fixture
def invalid_iata_code(get_airport):
    """
    Genera un IATA code que no existe en la API.
    """
    found = False
    while not found:
        iata_code = _random_iata_code()
        response = get_airport({"iata_code": iata_code})
        found = response.status_code == 404  # Solo se acepta si no existe
    return iata_code

# ======= Fixture para crear aeropuerto base temporal =======
@pytest.fixture
def create_base_airport(auth_headers):
    created = []

    def _create_base():
        payload = {
            "iata_code": "TMP",  # IATA temporal que no choque
            "city": "TestCity",
            "country": "TestCountry"
        }
        response = api_request("post", AIRPORTS, json=payload, headers=auth_headers)
        created.append(payload["iata_code"])
        return payload  # devolvemos el payload para usarlo en update

    yield _create_base

    # Cleanup después de cada test
    for code in created:
        api_request("delete", f"{AIRPORTS}/{code}", headers=auth_headers)

# ======= Fixture para actualizar aeropuerto =======
@pytest.fixture
def update_airport(auth_headers):
    def _update_airport(case, old_airport):
        iata_code = case.get("iata_code", old_airport["iata_code"])
        city = case.get("city", old_airport.get("city", ""))
        country = case.get("country", old_airport.get("country", ""))
        payload = {
            "iata_code": iata_code,
            "city": city,
            "country": country
        }
        response = api_request(
            "put",
            f"{AIRPORTS}/{old_airport['iata_code']}",
            json=payload,
            headers=auth_headers
        )
        return response
    return _update_airport

# ======= Fixture que combina creación y actualización =======
@pytest.fixture
def update_valid_airport(create_base_airport, update_airport):
    def _update_valid_airport(case):
        base_airport = create_base_airport()  # aeropuerto temporal
        response = update_airport(case, base_airport)
        print(f"Payload enviado: {case}, Status: {response.status_code}, Body: {response.text}")
        return response
    return _update_valid_airport

@pytest.fixture
def create_valid_airports(auth_headers,create_airports_case):
    def _create_valid_airports():
        airports = _valid_airports()
        response = create_airports_case(airports)
        return response.json()
    return _create_valid_airports

@pytest.fixture
def create_airports_case(auth_headers):
    def _create_airports_case(case):
        iata_code = case.get("iata_code", valid_iata_code)
        city = case.get("city", valid_city)
        country = case.get("country", valid_country)
        airport = {"iata_code": iata_code, "city": city, "country": country}
        response = api_request("post", AIRPORTS, headers=auth_headers, json=airport)
        return response
    return _create_airports_case

@pytest.fixture(scope="class")
def delete_airports(auth_headers):
    def _delete_airports(iata_code):
        url = f"{AIRPORTS}/{iata_code}"       # Construyes la URL
        print(f"[DEBUG] DELETE URL: {url}")  # 🔹 Imprime la URL
        response = api_request("delete", url, headers=auth_headers)
        return response
    return _delete_airports

@pytest.fixture
def list_airports(auth_headers,create_valid_airports):
    def _list_airports(skip,limit):
        _populate(skip + limit,create_valid_airports)
        response = api_request("get", AIRPORTS,params={"skip":skip,"limit":limit}, headers=auth_headers)
        return response
    return _list_airports

@pytest.fixture
def list_airports_without_params(auth_headers,create_valid_airports):
        _populate(1, create_valid_airports)
        response = api_request("get", AIRPORTS, headers=auth_headers)
        return response

@pytest.fixture(autouse=True)
def cleanup_airport(delete_airports):
    # Se ejecuta antes de cada test
    yield
    delete_airports(valid_iata_code)  # borra el aeropuerto creado