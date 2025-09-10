#   utils/settings.py

import faker

AIRPORTS = "/airports"
FLIGHTS = "/flights"
AUTH_LOGIN = "/auth/login/"
AUTH_SIGN_UP= "/auth/signup"
BASE_URL = "https://cf-automation-airline-api.onrender.com"
USERS = "/users/"
AIRCRAFTS = "/aircrafts"
BOOKINGS = "/bookings"

MAX_WAIT_SECONDS = 60
USERS_ME = "/users/me"

fake = faker.Faker()

airport_schema = {
    "type": "object",
    "required": ["iata_code", "city", "country"],
    "properties": {
        "iata_code": {"type": "string", "minLength": 3, "maxLength": 3},
        "city": {"type": "string"},
        "country": {"type": "string"},
    },
    "additionalProperties": True
}

user_schema = {
    "type": "object",
    "required": ["id", "email", "full_name", "role"],
    "properties": {
        "id": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "full_name": {"type": "string"},
        "role": {"type": "string", "enum": ["passenger", "admin"]}
    },
    "additionalProperties": True
}

aircraft_schema = {
    "type": "object",
    "required": ["tail_number","model","capacity","id"],
    "properties": {
        "tail_number": {"type": "string"},
        "model": {"type": "string"},
        "capacity": {"type": "integer"},
        "id": {"type": "string"},
    }
}

flight_schema = {
    "type": "object",
    "required": ["origin","destination","departure_time","arrival_time",
                 "base_price","aircraft_id","string","available_seats"],
    "properties": {
        "origin": {"type": "string", "minLength": 3, "maxLength": 3},
        "destination": {"type": "string", "minLength": 3, "maxLength": 3},
        "departure_time": { "type": "string", "format": "date-time" },
        "arrival_time": { "type": "string", "format": "date-time" },
        "base_price":  {"type": "integer"},
        "aircraft_id": {"type": "string"},
        "id": {"type": "string"},
        "available_seats": {"type": "integer"}
    },
    "additionalProperties": True
}

booking_schema = {
    "type": "object",
    "required": ["id", "flight_id", "user_id","status","passengers"],
    "properties": {
        "id": {"type": "string"},
        "flight_id": {"type": "string"},
        "user_id": {"type": "string"},
        "status": {"type": "string", "enum":["draft","paid","checked_in","cancelled"]},
        "passengers": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["full_name","passport"],
                "properties": {
                    "full_name": {"type": "string"},
                    "passport": {"type": "string"},
                    "seat": {"type": ["string", "null"]},
                }
            }
        }
    }
}