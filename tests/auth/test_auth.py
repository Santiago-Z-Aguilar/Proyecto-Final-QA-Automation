# tests/auth/test_auth.py
import os

import pytest
import logging
from tests.auth.data import emails_to_test, passwords_to_test, full_names_to_test, valid_password, valid_full_name
from jsonschema import validate
from utils.settings import user_schema
from utils.user_helpers import get_unique_email
from tests.auth.conftest import login, login_as_passenger


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qa_tests")

# EMAIL TESTS
@pytest.mark.parametrize("case", emails_to_test)
def test_signup_various_emails(signup_test_case, case):
    signup_test_case(
        {
            "email": case["email"],
            "password": valid_password,
            "full_name": valid_full_name,
            "expected_status": case["expected_status"]
        },
        variable="email"
    )

# PASSWORD TESTS
@pytest.mark.parametrize("case", passwords_to_test)
def test_signup_various_passwords(signup_test_case, case):
    unique_email = get_unique_email(prefix="pwtest")
    signup_test_case(
        {
            "email": unique_email,
            "password": case["password"],
            "full_name": valid_full_name,
            "expected_status": case["expected_status"]
        },
        variable="password"
    )

# FULL NAME TESTS
@pytest.mark.parametrize("case", full_names_to_test)
def test_signup_various_full_names(signup_test_case, case):
    resp, email, user = signup_test_case(case, variable="full_name")

    # Validación extra de normalización solo si aplica
    if case["expected_status"] == 201 and case.get("expected_user_created"):
        assert user, f"User with email '{email}' not found after signup."
        expected_name = case["expected_user_created"]
        real_name = user.get("full_name")
        assert real_name == expected_name, (
            f"Full name was not normalized as expected.\n"
            f"Sent: '{case['full_name']}' | Expected: '{expected_name}' | Got: '{real_name}'"
        )


def test_signup_with_forced_admin_role(signup_with_custom_role):
    user = signup_with_custom_role(role="admin")
    assert user.get("role") == "passenger"


def test_user_schema(signup_with_valid_data):
    validate(instance=signup_with_valid_data, schema=user_schema)


def test_login_as_admin():
    response = login(user=os.getenv("ADMIN_USER"), password=os.getenv("ADMIN_PASSWORD"))
    assert "access_token" in response.json()


def test_login_as_passenger(auth_headers):
    response = login_as_passenger(auth_headers)
    assert "access_token" in response.json()


def test_login_with_wrong_password():
    response = login(user=os.getenv("ADMIN_USER"), password="wrong_password")

    # Assert status code
    assert response.status_code == 401, (
        f"Expected 401, got {response.status_code}. Response: {response.text}"
    )

    # Parse JSON and assert error message
    data = response.json()
    assert data.get("detail") == "Incorrect credentials", (
        f"Expected 'Incorrect credentials', got: {data.get('detail')}"
    )


def test_login_with_unregistered_user():
    response = login(user="unregistered@test.com", password="any_password")

    # Assert status code
    assert response.status_code == 401, (
        f"Expected 401, got {response.status_code}. Response: {response.text}"
    )

    # Parse JSON and validate error structure
    data = response.json()
    assert isinstance(data, dict), "API should return a JSON dictionary"
    assert "detail" in data, "Response missing 'detail' field"

    # Flexible message check
    assert "credentials" in data["detail"].lower(), (
        f"Expected credential error, got: {data['detail']}"
    )