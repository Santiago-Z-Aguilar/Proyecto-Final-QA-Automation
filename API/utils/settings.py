#   utils/settings.py

import faker

AIRPORT = "/airports/"
AUTH_LOGIN = "/auth/login/"
AUTH_SIGN_UP= "/auth/signup"
BASE_URL = "https://cf-automation-airline-api.onrender.com"
USERS = "/users/"

MAX_WAIT_SECONDS = 60

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

