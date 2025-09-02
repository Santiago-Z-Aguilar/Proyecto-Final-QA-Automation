# tests/conftest.py
from API.tests.users.conftest import create_user_as_passenger
from API.utils.settings import AUTH_LOGIN, AUTH_SIGN_UP
from dotenv import load_dotenv
import os
import faker
from API.utils.user_helpers import _create_user, _build_user_data, delete_user_by_email
from API.utils.api_helpers import api_request
from API.utils.data import passenger_user_token_email

load_dotenv()

fake = faker.Faker()

import logging
import pytest

logger = logging.getLogger("Token_tests")


# ---------- Admin_token ----------

@pytest.fixture(scope="session")
def admin_token():
    user = os.getenv("ADMIN_USER")
    password = os.getenv("ADMIN_PASSWORD")

    response = api_request(
        "post", AUTH_LOGIN, data={"username": user, "password": password})

    if response is None:
        raise Exception("❌ Login failed after some retries")

    try:
        return response.json()["access_token"]
    except (KeyError, ValueError):
        raise Exception(f"❌ Login failed. Unexpected Response: {response.text}")

@pytest.fixture(scope="session")
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


# ---------- Passenger token ----------

@pytest.fixture(scope="session")
def passenger_token(admin_token):
    email = passenger_user_token_email
    user = email
    password = "PassengerPassword"
    full_name = "Passenger Token Jasy"

    payload = _build_user_data(email, password, full_name)

    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    _create_user(
        payload=payload,
        path=AUTH_SIGN_UP,
        auth_headers=admin_headers,
        treat_duplicate_as_success=True
    )

    response = api_request(
        "post", AUTH_LOGIN, data={"username": user, "password": password}
    )

    if response is None:
        raise Exception("❌ Login failed after some retries")

    try:
        token = response.json()["access_token"]
        yield token  # Entrega el token para su uso
    except (KeyError, ValueError):
        raise Exception(f"❌ Login failed. Unexpected Response: {response.text}")
    finally:
        # Cleanup después de que todas las pruebas usen el token
        delete_user_by_email(passenger_user_token_email, admin_headers)

@pytest.fixture(scope="session")
def passenger_headers(passenger_token):
    """Fixture de test que da headers, depende del session para cleanup."""
    return {"Authorization": f"Bearer {passenger_token}"}
