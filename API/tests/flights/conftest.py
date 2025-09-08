from API.utils.api_helpers import api_request
from API.tests.aircrafts.conftest import create_valid_aircraft
import pytest
from API.utils.settings import FLIGHTS

#@pytest.fixture
#def create_flight(auth_headers,create_valid_aircraft):
#    aircraft = create_valid_aircraft()
#    flight = {
#        "origin": "NIU",
#        "destination": "AKM",
#        "departure_time": "2025-09-02 18:10:15",
#        "arrival_time": "2025-09-02T18:54:14.225Z",
#        "base_price": 0,
#        "aircraft_id": aircraft["id"]
#    }
#    response = api_request("post",path=FLIGHTS,headers=auth_headers,json=flight)
#   return response.json()



#Se puede borrar esto