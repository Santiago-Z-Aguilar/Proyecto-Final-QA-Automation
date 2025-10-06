from API.utils.api_helpers import api_request
from API.utils.data import valid_tail_number, valid_capacity, valid_model
from API.utils.settings import AIRCRAFTS
import pytest,string,random
from API.utils.aircrafts_helpers import valid_aircraft





def _random_aircraft_id():
    first = ''.join(random.choices(string.ascii_lowercase, k=3))
    second = '-'.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return first + second

def _populate(aircrafts_needed,create_valid_aircraft):
    for i in range(0,aircrafts_needed):
        create_valid_aircraft()

@pytest.fixture
def get_aircraft(auth_headers):
    def _get_aircraft(aircraft_id):
        response = api_request("get",f"{AIRCRAFTS}/{aircraft_id}", headers=auth_headers)
        return response
    return _get_aircraft

@pytest.fixture
def update_aircraft(auth_headers):
    def _update_aircraft_case(case,old_aircraft):
         tail_number = case.get("tail_number", old_aircraft["tail_number"])
         capacity = case.get("capacity", old_aircraft["capacity"])
         model = case.get("model", old_aircraft["model"])
         aircraft = {"tail_number": tail_number, "model": model, "capacity": capacity}
         response = api_request("put", f"{AIRCRAFTS}/{old_aircraft["id"]}", headers=auth_headers, json=aircraft)
         return response
    return _update_aircraft_case

@pytest.fixture
def update_valid_aircraft(auth_headers,create_valid_aircraft,update_aircraft):
    def _update_valid_aircraft(case):
        aircraft = create_valid_aircraft()
        response = update_aircraft(case,aircraft)
        return response
    return _update_valid_aircraft


@pytest.fixture
def create_valid_aircraft(auth_headers,create_aircraft_case):
    def _create_valid_aircraft():
        aircraft = valid_aircraft()
        response = create_aircraft_case(aircraft)
        return response.json()
    return _create_valid_aircraft

@pytest.fixture
def create_aircraft_case(auth_headers):
    def _create_aircraft_case(case):
        tail_number = case.get("tail_number", valid_tail_number)
        capacity = case.get("capacity", valid_capacity)
        model = case.get("model", valid_model)
        aircraft = {"tail_number": tail_number, "model": model, "capacity": capacity}
        response = api_request("post", AIRCRAFTS, headers=auth_headers, json=aircraft)
        return response
    return _create_aircraft_case

@pytest.fixture
def delete_aircraft(auth_headers):
    def _delete_aircraft(aircraft_id):
        response = api_request("delete", f"{AIRCRAFTS}/{aircraft_id}", headers=auth_headers)
        return response
    return _delete_aircraft

@pytest.fixture
def invalid_aircraft_id(get_aircraft):
    found = False
    while not found:
        aircraft_id = _random_aircraft_id()
        response = get_aircraft(aircraft_id)
        found = response.status_code == 404
    return aircraft_id

@pytest.fixture
def list_aircrafts(auth_headers,create_valid_aircraft):
    def _list_aircrafts(skip,limit):
        _populate(skip + limit,create_valid_aircraft)
        response = api_request("get", AIRCRAFTS,params={"skip":skip,"limit":limit}, headers=auth_headers)
        return response
    return _list_aircrafts

@pytest.fixture
def list_aircrafts_without_params(auth_headers,create_valid_aircraft):
        _populate(1, create_valid_aircraft)
        response = api_request("get", AIRCRAFTS, headers=auth_headers)
        return response

