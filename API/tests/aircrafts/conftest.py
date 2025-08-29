from API.utils.api_helpers import api_request
from API.utils.data import valid_tail_number, valid_capacity, valid_model
from API.utils.settings import AIRCRAFTS
import pytest


#def _create_aircraft(auth_headers):

def _create_aircraft_case(case,auth_headers):
    tail_number = case.get("tail_number",valid_tail_number)
    capacity = case.get("capacity",valid_capacity)
    model = case.get("model",valid_model)
    aircraft = \
        {"tail_number": tail_number,
                    "model": model,
                    "capacity": capacity}
    response = api_request("post", AIRCRAFTS, headers=auth_headers, json=aircraft)
    return response

@pytest.fixture
def create_aircraft_tail_number_case(auth_headers):
    def _create_aircraft_tail_number(case):
        return _create_aircraft_case(case, auth_headers)
    return _create_aircraft_tail_number

@pytest.fixture
def create_aircraft_capacity_case(auth_headers):
    def _create_aircraft_capacity(case):
        return _create_aircraft_case(case, auth_headers)
    return _create_aircraft_capacity

@pytest.fixture
def create_aircraft_model_case(auth_headers):
    def _create_aircraft_model(case):
        return _create_aircraft_case(case, auth_headers)
    return _create_aircraft_model