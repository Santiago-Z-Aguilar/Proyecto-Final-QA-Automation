# tests/conftest.py

from utils.settings import BASE_URL, AUTH_LOGIN, USERS, AUTH_SIGN_UP
from dotenv import load_dotenv
import os
import pytest
import faker
import time

from utils.api_helpers import api_request

load_dotenv()

fake = faker.Faker()

@pytest.fixture(scope="session")
def admin_token():
    user = os.getenv("ADMIN_USER")
    pwd = os.getenv("ADMIN_PASSWORD")

    response = api_request(
        "post", AUTH_LOGIN, data={"username": user, "password": pwd})

    if response is None:
        raise Exception("❌ Login failed after some retries")

    try:
        return response.json()["access_token"]
    except (KeyError, ValueError):
        raise Exception(f"❌ Login failed. Unexpected Response: {response.text}")

@pytest.fixture
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}

def test_auth_headers(admin_token):
    r = admin_token
    return r
