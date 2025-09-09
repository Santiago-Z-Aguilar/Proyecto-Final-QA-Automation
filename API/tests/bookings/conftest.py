import json

from API.utils.api_helpers import api_request
from API.utils.flights_helpers import create_valid_flight
import pytest
from API.utils.settings import BOOKINGS
from API.utils.bookings_helpers import valid_booking
from API.utils.data import one_passenger_payload,valid_full_name


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

@pytest.fixture
def list_bookings(auth_headers):
    def _list_bookings(skip,limit):
        if limit is None and skip is None:
            response = api_request(method="GET",path=BOOKINGS,headers=auth_headers)
        else:
            response = api_request(method="GET", path=BOOKINGS,params={"skip":skip,"limit":limit}, headers=auth_headers)
        return response
    return _list_bookings

@pytest.fixture
def get_booking():
    def _get_booking(booking_id,headers):
        response = api_request(method="GET", path=f"{BOOKINGS}/{booking_id}",headers=headers)
        return response
    return _get_booking

@pytest.fixture
def update_booking():
    def _update_booking(booking_id,update_case,headers):
        response = api_request(method="PATCH", path=f"{BOOKINGS}/{booking_id}",json=update_case,headers=headers)
        return response
    return _update_booking

@pytest.fixture
def delete_booking():
    def _delete_booking(booking_id,headers):
        response = api_request(method="DELETE", path=f"{BOOKINGS}/{booking_id}",headers=headers)
        return response
    return _delete_booking

@pytest.fixture
def create_valid_booking_as_passenger(passenger_headers,auth_headers):
    flight = create_valid_flight(auth_headers)
    booking_payload = valid_booking(flight)
    booking = api_request(method="POST", path=BOOKINGS, headers=passenger_headers, json=booking_payload).json()
    return booking


