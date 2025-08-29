import os
import pytest
from jsonschema import validate
from API.utils.data import tail_numbers_to_test

class TestAircraftValidation:
    @pytest.mark.parametrize("tail_number_case",tail_numbers_to_test)
    def test_create_aircraft(self,create_aircraft_tail_number_case, tail_number_case):
        response = create_aircraft_tail_number_case(tail_number_case)
        assert response.status_code == tail_number_case["expected_status"]




