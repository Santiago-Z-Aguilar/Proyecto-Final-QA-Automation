import os
import pytest
from jsonschema import validate
from API.utils.data import valid_iata_code, iata_code_to_test,city_to_test, country_to_test, pagination_values_to_test, capacities_to_test, models_to_test
from API.utils.settings import aircraft_schema, airport_schema

class TestAirports:

    #--- POST /airports OK
    @pytest.mark.parametrize("iata_code_case",iata_code_to_test)
    def test_create_iata_code_validation(self,create_airports_case, iata_code_case):
        response = create_airports_case(iata_code_case)
        assert response.status_code == iata_code_case["expected_status"]

    @pytest.mark.parametrize("city_case", city_to_test)
    def test_create_city_validation(self, create_airports_case, city_case):
        response = create_airports_case(city_case)
        assert response.status_code == city_case["expected_status"]

    @pytest.mark.parametrize("country_case", country_to_test)
    def test_create_country_validation(self, create_airports_case, country_case):
        response = create_airports_case(country_case)
        assert response.status_code == country_case["expected_status"]

    #--- GET /airports  OK
    @pytest.mark.parametrize("pagination_values",pagination_values_to_test)
    def test_list_airports(self,list_airports,pagination_values):
        response = list_airports(skip=pagination_values["skip"],limit=pagination_values["limit"])
        print("\nRESPONSE STATUS:", response.status_code)
        print("RESPONSE BODY:", response.json())  # si es JSON
        assert response.status_code == pagination_values["expected_status"]

    def test_list_airports_without_params(self,list_airports_without_params):
        print("\nRESPONSE STATUS:", list_airports_without_params.status_code)
        print("RESPONSE BODY:", list_airports_without_params.json())  # si es JSON
        assert list_airports_without_params.status_code == 200

    #--- GET /airports/{iata_code} OK
    def test_get_airport(self, create_valid_airports, get_airport):
        airport = create_valid_airports()  # Crea un aeropuerto de prueba
        response = get_airport(airport)  # Pasa el diccionario completo
        print("[DEBUG] RESPONSE BODY:", response.json())  # Para ver la respuesta completa
        assert response.json() == airport

    def test_get_invalid_airport(self, invalid_iata_code, get_airport):
        response = get_airport({"iata_code": invalid_iata_code})
        print("[DEBUG] RESPONSE IATA CODE INVALID STATUS:", response.status_code)
        print("[DEBUG] RESPONSE IATA CODE INVALID BODY:", response.json())
        assert response.status_code == 404

    # --- PUT /airports/{iata_code} iata_code validation OK
    @pytest.mark.parametrize("iata_code_case", iata_code_to_test)
    def test_update_iata_code_validation(self, update_valid_airport, iata_code_case):
        # Normalizamos status 201 -> 200 si es necesario
        if iata_code_case["expected_status"] == 201:
            iata_code_case["expected_status"] = 200
        response = update_valid_airport(iata_code_case)
        assert response.status_code == iata_code_case["expected_status"]

    # --- PUT /airports/{iata_code} city validation OK
    @pytest.mark.parametrize("city_case", city_to_test)
    def test_update_city_validation(self, update_valid_airport, city_case):
        # Ajuste del expected_status si viene 201
        if city_case["expected_status"] == 201:
            city_case["expected_status"] = 200
        # Llamamos al fixture pasando solo la propiedad city
        response = update_valid_airport({"city": city_case["city"]})
        # Imprimir información útil
        print(
            f"Payload enviado: {{'city': {city_case['city']}}}, Status: {response.status_code}, Body: {response.text}")
        # Validar status code
        assert response.status_code == city_case["expected_status"]

    # --- PUT /airports/{iata_code} country validation OK
    @pytest.mark.parametrize("country_case", country_to_test)
    def test_update_country_validation(self, update_valid_airport, country_case):
        # Ajuste del expected_status si viene 201
        if country_case["expected_status"] == 201:
            country_case["expected_status"] = 200
        # Llamamos al fixture pasando solo la propiedad country
        response = update_valid_airport({"country": country_case["country"]})
        # Imprimir información útil
        print(
            f"Payload enviado: {{'country': {country_case['country']}}}, Status: {response.status_code}, Body: {response.text}")
        # Validar status code
        assert response.status_code == country_case["expected_status"]

    #--- DELETE /airports/aita_code OK
    def test_delete_valid_airport(self, delete_airports):
        response = delete_airports(valid_iata_code)  # aquí le pasas el iata_code
        assert response.status_code == 204

    def test_delete_invalid_airport(self,invalid_iata_code,delete_airports):
        airport = invalid_iata_code
        response = delete_airports(airport)
        assert response.status_code == 204 #204 No Content. El recurso no existe, la operación se considera exitosa

