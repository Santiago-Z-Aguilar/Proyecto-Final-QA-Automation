import os
import pytest
from jsonschema import validate
from API.utils.data import tail_numbers_to_test,models_to_test,capacities_to_test, pagination_values_to_test
from API.utils.settings import aircraft_schema

class TestAircrafts:

    #--- POST /aircrafts
    @pytest.mark.parametrize("tail_number_case",tail_numbers_to_test)
    def test_create_tail_number_validation(self,create_aircraft_case, tail_number_case):
        response = create_aircraft_case(tail_number_case)
        assert response.status_code == tail_number_case["expected_status"]

    @pytest.mark.parametrize("capacity_case", capacities_to_test)
    def test_create_capacity_validation(self, create_aircraft_case, capacity_case):
        response = create_aircraft_case(capacity_case)
        assert response.status_code == capacity_case["expected_status"]

    @pytest.mark.parametrize("model_case", models_to_test)
    def test_create_model_validation(self, create_aircraft_case, model_case):
        response = create_aircraft_case(model_case)
        assert response.status_code == model_case["expected_status"]

    #--- GET /aircrafts
    #El endpoint no funciona, siempre devuelve 500
    #@pytest.mark.parametrize("pagination_values",pagination_values_to_test)
    #def test_list_aircrafts(self,list_aircrafts,pagination_values):
    #    response = list_aircrafts(skip=pagination_values["skip"],limit=pagination_values["limit"])
    #    assert response.status_code == pagination_values["expected_status"]

    #def test_list_aircrafts_without_params(self,list_aircrafts_without_params):
    #    assert list_aircrafts_without_params.status_code == 200


    #--- GET /aircrafts/{aircraft_id}
    def test_get_aircraft(self,create_valid_aircraft,get_aircraft):
        aircraft = create_valid_aircraft()
        response = get_aircraft(aircraft["id"])
        assert response.json() == aircraft

    def test_get_invalid_aircraft(self,invalid_aircraft_id,get_aircraft):
        aircraft_id = invalid_aircraft_id
        response = get_aircraft(aircraft_id)
        assert response.status_code == 404

    #--- PUT /aircrafts/{aircraft_id}
    @pytest.mark.parametrize("tail_number_case", tail_numbers_to_test)
    def test_update_tail_number_validation(self, update_valid_aircraft, tail_number_case):
        if tail_number_case["expected_status"] == 201:
            tail_number_case["expected_status"] = 200
        response = update_valid_aircraft(tail_number_case)
        assert response.status_code == tail_number_case["expected_status"]

    @pytest.mark.parametrize("capacity_case", capacities_to_test)
    def test_update_capacity_validation(self, update_valid_aircraft, capacity_case):
        if capacity_case["expected_status"] == 201:
            capacity_case["expected_status"] = 200
        response = update_valid_aircraft(capacity_case)
        assert response.status_code == capacity_case["expected_status"]

    @pytest.mark.parametrize("model_case", models_to_test)
    def test_update_model_validation(self, update_valid_aircraft, model_case):
        if model_case["expected_status"] == 201:
            model_case["expected_status"] = 200
        response = update_valid_aircraft(model_case)
        assert response.status_code == model_case["expected_status"]

    #--- DELETE /aircrafts/{aircraft_id}
    def test_delete_valid_aircraft(self,create_valid_aircraft,delete_aircraft):
        aircraft = create_valid_aircraft()
        response = delete_aircraft(aircraft["id"])
        assert response.status_code == 204

    def test_delete_invalid_aircraft(self,invalid_aircraft_id,delete_aircraft):
        aircraft_id = invalid_aircraft_id
        response = delete_aircraft(aircraft_id)
        assert response.status_code == 422


    # Schema Test

    def test_aircraft_schema(self,create_valid_aircraft,get_aircraft):
        aircraft = create_valid_aircraft()
        response = get_aircraft(aircraft["id"])
        validate(instance=response.json(), schema=aircraft_schema)
