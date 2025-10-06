import pytest
import uuid
from API.utils.api_helpers import api_request
from API.tests.aircrafts.conftest import create_valid_aircraft
from API.utils.settings import FLIGHTS
from API.utils.flights_helpers import *
from API.tests.flights.data_fligths import *
from API.utils.aircrafts_helpers import *



# -------------------------
# Aircraft fixtures
# -------------------------
@pytest.fixture
def valid_aircraft_id(auth_headers):
    """
    Create an aircraft and return its ID to associate it with a flight.
    """
    response = create_valid_aircraft(auth_headers)
    return response["id"]


@pytest.fixture
def nonexistent_aircraft_id():
    """Generates a non-existent aircraft_id (valid format but not in DB)."""
    return f"acf-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def empty_aircraft_id():
    """Returns an empty aircraft_id."""
    return ""


@pytest.fixture
def numeric_aircraft_id():
    """Generates an invalid numeric aircraft_id."""
    return "123456"


# -------------------------
# Flight fixtures
# -------------------------
@pytest.fixture
def base_flight_data(valid_aircraft_id):
    """
    Returns a valid flight data payload with a dynamic aircraft_id.
    """
    return build_flight_data(
        origin=valid_iata_origin,
        destination=valid_iata_destination,
        departure=datetime_today,
        arrival=datetime_future,
        base_price=base_price_valid,
        aircraft_id=valid_aircraft_id,
    )


@pytest.fixture
def create_flight(auth_headers):
    """
    Creates a new flight with a valid aircraft.
    Useful for booking or GET/PUT tests.
    """
    aircraft = create_valid_aircraft(auth_headers)
    flight = {
        "origin": "NIU",
        "destination": "AKM",
        "departure_time": "2025-09-02 18:10:15",
        "arrival_time": "2025-09-02T18:54:14.225Z",
        "base_price": 0,
        "aircraft_id": aircraft["id"],
    }
    response = api_request("post", path=FLIGHTS, headers=auth_headers, json=flight)
    return response.json()


@pytest.fixture
def flight_id(create_flight):
    """Returns only the id of a created flight."""
    return create_flight["id"]


# -------------------------
# Payload injection helpers
# -------------------------
@pytest.fixture
def with_aircraft_id(valid_aircraft_id):
    """
    Injects a valid aircraft_id into any payload.
    Usage in tests:
        payload = with_aircraft_id(data_template)
    """
    def _inject(data_template: dict):
        payload = data_template.copy()
        payload["aircraft_id"] = valid_aircraft_id
        return payload

    return _inject


# -------------------------
# Fake / invalid flight IDs
# -------------------------
@pytest.fixture
def fake_flight_id():
    """Generates a fake but validly formatted flight_id."""
    return f"flt-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def invalid_flight_id():
    """Generates an invalid flight_id (wrong format)."""
    return "12345-invalid-id"