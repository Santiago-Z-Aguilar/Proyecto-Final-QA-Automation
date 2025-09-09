from API.utils.settings import BOOKINGS
from API.utils.flights_helpers import create_valid_flight
from API.utils.api_helpers import api_request
from API.utils.data import valid_full_name

def create_valid_booking(auth_headers):
    flight = create_valid_flight(auth_headers)
    booking = valid_booking(flight)
    response = api_request(method="POST",path=BOOKINGS,headers=auth_headers,json=booking)
    return response.json()

def valid_booking(flight):
    booking = {
        "flight_id": flight["id"],
        "passengers": [
            {
                "full_name": valid_full_name,
                "passport": "string",
                "seat": "12"
            }]}
    return booking