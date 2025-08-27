from API.utils.api_helpers import api_request
from API.utils.settings import AIRCRAFTS
import pytest


#def _create_aircraft(auth_headers):



@pytest.fixture
def create_aircraft(auth_headers):
    aircraft = {"tail_number": "unodostres",
                "model": "modelon",
                "capacity": 500}
    response = api_request("post", AIRCRAFTS, headers=auth_headers, json=aircraft)
    return response