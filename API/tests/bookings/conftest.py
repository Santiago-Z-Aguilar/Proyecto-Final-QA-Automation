import json

from API.utils.api_helpers import api_request
from API.tests.flights.conftest import create_flight
import pytest
from API.utils.settings import BOOKINGS

@pytest.fixture
def create_booking(auth_headers,create_flight):
    flight = create_flight()
    booking = {
     "flight_id": "flt-233ebd4c",
    "passengers": [
        {
        "full_name": "string",
        "passport": "string",
        "seat": "12"
        }]}
    response = api_request(method="POST",path=BOOKINGS,headers=auth_headers,data=booking)
    return response
