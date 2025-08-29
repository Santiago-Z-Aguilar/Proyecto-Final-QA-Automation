from API.utils.api_helpers import api_request
from API.utils.settings import AIRCRAFTS
import pytest


#def _create_aircraft(auth_headers):



@pytest.fixture
def create_aircraft_tail_number_case(auth_headers):
    def _create_aircraft_tail_number(case):
        aircraft = {"tail_number": case["tail_number"],
                    "model": "modelon",
                    "capacity": 500}
        response = api_request("post", AIRCRAFTS, headers=auth_headers, json=aircraft)
        return response
    return _create_aircraft_tail_number