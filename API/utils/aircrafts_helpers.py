from API.utils.data import valid_tail_number,valid_model,valid_capacity
from API.utils.api_helpers import api_request
import pytest
from API.utils.settings import AIRCRAFTS

def valid_aircraft():
    return {"tail_number": valid_tail_number, "model": valid_model, "capacity": valid_capacity}

def create_aircraft_case(auth_headers,case):
    tail_number = case.get("tail_number", valid_tail_number)
    capacity = case.get("capacity", valid_capacity)
    model = case.get("model", valid_model)
    aircraft = {"tail_number": tail_number, "model": model, "capacity": capacity}
    response = api_request("post", AIRCRAFTS, headers=auth_headers, json=aircraft)
    return response

def create_valid_aircraft(auth_headers):
    aircraft = valid_aircraft()
    response = create_aircraft_case(auth_headers,aircraft)
    return response.json()