# utils/flight_helpers.py
import logging
import requests
from typing import Dict, Any, Optional
from API.utils.settings import FLIGHTS
from API.utils.aircrafts_helpers import create_valid_aircraft
from API.utils.api_helpers import api_request

logger = logging.getLogger("qa_tests")

def _build_flight_data(origin: str, destination: str, departure: str, arrival: str,
                       base_price: float, aircraft_id: str) -> Dict[str, Any]:
    #Construye payload estándar para vuelos.
    return {
        "origin": origin,
        "destination": destination,
        "departure_time": departure,
        "arrival_time": arrival,
        "base_price": base_price,
        "aircraft_id": aircraft_id
    }

def create_flight(payload: Dict[str, Any],auth_headers):
    resp = api_request("post", FLIGHTS, headers=auth_headers(), json=payload)
    #resp = requests.post(f"{base_url}{FLIGHTS}", json=payload, headers=headers)
    return resp

def delete_flight(id: str):
    resp = api_request("delete", FLIGHTS + "/" + id, headers=auth_headers())
    return resp

def get_flight_by_id(id: str) -> Optional[Dict]:
    resp = api_request("get", FLIGHTS + "/" + id)
    return resp

def create_valid_flight(auth_headers):
    valid_aircraft = create_valid_aircraft(auth_headers)
    flight = _build_flight_data(origin="NIU",destination="AKM",departure="2025-09-02 18:10:15",arrival="2025-09-02T18:54:14",base_price=2000,aircraft_id=valid_aircraft["id"])
    return create_flight(flight,auth_headers)


