# tests/auth/test_auth.py
import os
import pytest
from jsonschema import validate

from API.utils.data import valid_password, valid_full_name
from API.tests.auth.data_auth import (
    emails_to_test_signup,
    passwords_to_test_signup,
    full_names_to_test_signup,
)
from API.utils.user_helpers import create_user_with_email_already_registered
from API.utils.settings import user_schema, AUTH_SIGN_UP
from API.tests.auth.conftest import login, login_as_passenger


class TestEmailValidation:
    @pytest.mark.parametrize("email, expected_status", emails_to_test_signup.items())
    def test_email_validation(self, signup_email_case, email, expected_status):
        resp, expected, _ = signup_email_case({
            "email": email,
            "password": valid_password,
            "full_name": valid_full_name,
            "expected_status": expected_status,
        })
        assert resp.status_code == expected, f"Expected {expected}, got {resp.status_code}. Email: {email}. Body: {resp.text}"

class TestPasswordValidation:
    @pytest.mark.parametrize("password, expected_status", passwords_to_test_signup.items())
    def test_password_validation(self, signup_password_case, password, expected_status):
        resp, expected, _ = signup_password_case({
            "password": password,
            "full_name": valid_full_name,
            "expected_status": expected_status,
        })
        assert resp.status_code == expected, f"Expected {expected}, got {resp.status_code}. Body: {resp.text}"

class TestFullNameValidation:
    @pytest.mark.parametrize("name_case", full_names_to_test_signup)
    def test_name_validation(self, signup_full_name_case, name_case):
        case_data = {
            "full_name": name_case["full_name"],
            "expected_status": name_case["expected_status"],
        }
        if "password" in name_case:
            case_data["password"] = name_case["password"]

        resp, expected, user = signup_full_name_case(case_data)
        assert resp.status_code == expected, f"Expected {expected}, got {resp.status_code}. Body: {resp.text}"

        if expected == 201 and "expected_user_created" in name_case:
            assert user is not None, "Expected a created user object."
            assert user.get("full_name") == name_case["expected_user_created"], (
                f"Expected '{name_case['expected_user_created']}', got '{user.get('full_name')}'."
            )


def test_signup_with_existing_user(auth_headers):
    """Attempt to sign up twice with the same email and assert duplicate error."""
    status_code, detail = create_user_with_email_already_registered(
        auth_headers, AUTH_SIGN_UP, role="admin"
    )
    assert status_code == 400
    assert "already registered" in str(detail).lower(), (
        f"Expected 'already registered' in error, but got '{detail}'"
    )


def test_admin_role_converted_to_passenger(signup_with_custom_role):
    """Creating a user with role='admin' at signup must be coerced to 'passenger'."""
    user = signup_with_custom_role(role="admin")
    assert user["role"] == "passenger", (
        f"Expected role 'passenger' but got '{user['role']}'"
    )


def test_user_schema_validation(signup_with_valid_data):
    """Validate the created user object matches the JSON schema."""
    validate(instance=signup_with_valid_data, schema=user_schema)


class TestLoginFunctionality:
    def test_admin_login(self):
        """Admin credentials should return an access token."""
        response = login(
            user=os.getenv("ADMIN_USER"),
            password=os.getenv("ADMIN_PASSWORD"),
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_passenger_login(self, auth_headers):
        """Passenger signup + login flow should return an access token."""
        response = login_as_passenger(auth_headers)
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_with_invalid_credentials(self):
        """Wrong password should return 401 with a safe error message."""
        response = login(
            user=os.getenv("ADMIN_USER"),
            password="wrong_password",
        )
        assert response.status_code == 401
        assert response.json().get("detail") == "Incorrect credentials"

    def test_login_with_unregistered_user(self):
        """Unregistered user should return 401 without leaking field-specific hints."""
        response = login(
            user="unregistered@test.com",
            password="any_password",
        )
        assert response.status_code == 401
        detail = response.json().get("detail", "")
        assert "password" not in str(detail).lower()
        assert "email" not in str(detail).lower()
