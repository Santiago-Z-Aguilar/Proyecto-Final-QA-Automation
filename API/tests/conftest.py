# tests/conftest.py

from API.utils.settings import AUTH_LOGIN
from dotenv import load_dotenv
import os
import faker

from API.utils.api_helpers import api_request

load_dotenv()

fake = faker.Faker()

import logging
import pytest

logger = logging.getLogger("qa_tests")


# ---------- Fixtures ----------

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

# def test_auth_headers(admin_token):
#     r = admin_token
#     return r


