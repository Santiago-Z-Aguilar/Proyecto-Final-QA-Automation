# utils/flight_helpers.py
import logging
import requests
from typing import Dict, Any, Optional
from API.utils.settings import FLIGHTS

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
    resp = api_requests("post", FLIGHTS, headers=auth_headers(), json=payload)
    #resp = requests.post(f"{base_url}{FLIGHTS}", json=payload, headers=headers)
    return resp

def delete_flight(id: str):
    resp = api_requests("delete", FLIGHTS + "/" + id, headers=auth_headers())
    return resp

def get_flight_by_id(id: str) -> Optional[Dict]:
    resp = api_requests("get", FLIGHTS + "/" + id)
    return resp