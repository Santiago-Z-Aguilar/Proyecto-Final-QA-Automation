# utils/flight_helpers.py
import logging
import requests
from typing import Dict, Any, Optional
from API.utils.settings import *
from API.utils.api_helpers import *
from API.utils.aircrafts_helpers import create_valid_aircraft

logger = logging.getLogger("qa_tests")

# ---------- Payload builders ----------
def build_flight_data(origin: str, destination: str, departure: str, arrival: str,
                       base_price: float, aircraft_id: str) -> Dict[str, Any]:
    """Construye un payload estándar para vuelos."""
    return {
        "origin": origin,
        "destination": destination,
        "departure_time": departure,
        "arrival_time": arrival,
        "base_price": base_price,
        "aircraft_id": aircraft_id
    }

# def build_aircraft(tail_number="N123CC",
#                    model="Boeing 737-800", capacity=200)-> Dict[str, Any]:
#     # Construye payload estándar para vuelos.
#     return {
#         "tail_number": tail_number,
#         "model": model,
#         "capacity": capacity,
#     }


# ---------- API actions ----------
def create_flight(payload: Dict[str, Any], auth_headers)-> Optional[Dict]:
    return api_request("post", FLIGHTS, headers=auth_headers, json=payload)


def delete_flight(id: str, auth_headers):
    return api_request("delete", FLIGHTS + "/" + id, headers=auth_headers)


def get_flight_by_id(id: str) -> Optional[Dict]:
    return api_request("get", FLIGHTS + "/" + id)


def get_flights() -> Optional[Dict]:
    print("STATUS: getfligths")
    return api_request("get", FLIGHTS)

# def create_aircraft(auth_headers)-> Optional[Dict]:
#     aircraft = build_aircraft()
#     return api_request("post", AIRCRAFTS, headers=auth_headers, json=aircraft)

def update_flight(id: str, payload: Dict[str, Any], auth_headers) -> Optional[Dict]:
    return api_request("put", FLIGHTS + "/" + id, headers=auth_headers, json=payload)


#----- asserciones negativas
def assert_response(resp, expected_status: int):
    """
    Valida el status code de una respuesta y devuelve el JSON.
    Si falla, muestra el body completo en el mensaje de error.
    """
    status_code = resp.status_code
    try:
        detail = resp.json()
    except Exception:
        detail = resp.text  # fallback si no es JSON

    assert status_code != expected_status, (
        f"Expected {expected_status}, got {status_code}. Response: {detail}"
    )

    return detail

def create_valid_flight(auth_headers):
    valid_aircraft = create_valid_aircraft(auth_headers)
    flight = build_flight_data(origin="NIU",destination="AKM",departure="2025-09-02 18:10:15",arrival="2025-09-02T18:54:14",base_price=2000,aircraft_id=valid_aircraft["id"])
    return create_flight(flight,auth_headers).json()