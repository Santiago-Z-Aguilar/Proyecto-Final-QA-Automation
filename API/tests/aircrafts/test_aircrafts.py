import os
import pytest
from jsonschema import validate
from API.utils.data import tail_numbers_to_test,models_to_test,capacities_to_test

class TestAircrafts:
    @pytest.mark.parametrize("tail_number_case",tail_numbers_to_test)
    def test_create_tail_number_validation(self,create_aircraft_tail_number_case, tail_number_case):
        response = create_aircraft_tail_number_case(tail_number_case)
        assert response.status_code == tail_number_case["expected_status"]

    @pytest.mark.parametrize("capacity_case", capacities_to_test)
    def test_create_capacity_validation(self, create_aircraft_capacity_case, capacity_case):
        response = create_aircraft_capacity_case(capacity_case)
        assert response.status_code == capacity_case["expected_status"]

    @pytest.mark.parametrize("model_case", models_to_test)
    def test_create_model_validation(self, create_aircraft_model_case, model_case):
        response = create_aircraft_model_case(model_case)
        assert response.status_code == model_case["expected_status"]



