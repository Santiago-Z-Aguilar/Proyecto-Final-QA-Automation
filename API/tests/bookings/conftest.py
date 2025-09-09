import json

from API.utils.api_helpers import api_request
from API.utils.flights_helpers import create_valid_flight
import pytest
from API.utils.settings import BOOKINGS
from API.utils.data import one_passenger_payload


def _create_booking(auth_headers,flight_id,passengers):
    booking = {
        "passengers": passengers
    }
    if flight_id is not None:
        booking["flight_id"] = flight_id
    response = api_request(method="POST",path=BOOKINGS,headers=auth_headers,json=booking)
    return response

@pytest.fixture
def create_booking_passenger_case(auth_headers):
    def _create_booking_passenger_case(passenger_case):
        flight = create_valid_flight(auth_headers)
        response = _create_booking(auth_headers,flight["id"],passenger_case)
        return response
    return _create_booking_passenger_case

@pytest.fixture
def create_booking_flight_case(auth_headers):
    def _create_booking_flight_case(flight_case):
        response = _create_booking(auth_headers,flight_case,one_passenger_payload)
        return response
    return _create_booking_flight_case