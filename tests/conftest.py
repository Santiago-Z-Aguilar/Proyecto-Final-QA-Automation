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

import logging
import pytest

logger = logging.getLogger("qa_tests")

def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """
    Emit a clear error log whenever a test fails, with nodeid and a short traceback.
    This complements assertion-local logging and helps when failures happen outside our asserts.
    """
    report = pytest.TestReport.from_item_and_call(item, call)
    if report.when in ("call", "setup", "teardown") and report.failed:
        # Short style keeps output compact; change to 'long' if you want full trace here.
        short_tb = call.excinfo.getrepr(style="short") if call.excinfo else "<no excinfo>"
        logger.error("TEST FAILED: %s\n%s", item.nodeid, short_tb)
    return report


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
