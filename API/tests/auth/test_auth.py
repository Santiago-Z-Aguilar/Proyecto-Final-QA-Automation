# tests/auth/test_auth.py

import os
import pytest
from jsonschema import validate
from API.utils.data import (
    emails_to_test,
    passwords_to_test,
    full_names_to_test,
    valid_password,
    valid_full_name,
)
from API.utils.user_helpers import create_user_with_email_already_registered
from API.utils.settings import user_schema, AUTH_SIGN_UP
from API.tests.auth.conftest import login, login_as_passenger


# ---------- Email tests ----------
class TestEmailValidation:

    @pytest.mark.parametrize("email, expected_status", emails_to_test.items())
    def test_email_validation(self, signup_email_case, email, expected_status):
        signup_email_case({
            "email": email,
            "password": valid_password,
            "full_name": valid_full_name,
            "expected_status": expected_status,
        })


# ---------- Password tests ----------
class TestPasswordValidation:

    @pytest.mark.parametrize("password, expected_status", passwords_to_test.items())
    def test_password_validation(self, signup_password_case, password, expected_status):
        signup_password_case({
            "password": password,
            "full_name": valid_full_name,
            "expected_status": expected_status,
        })


# ---------- Full name tests ----------
class TestFullNameValidation:
    @pytest.mark.parametrize("name_case", full_names_to_test)
    def test_name_validation(self, signup_full_name_case, name_case):
        case_data = {
            "full_name": name_case["full_name"],
            "expected_status": name_case["expected_status"]
        }
        if "password" in name_case:
            case_data["password"] = name_case["password"]

        resp, email, user = signup_full_name_case(case_data)

        if name_case["expected_status"] == 201 and "expected_user_created" in name_case:
            assert user["full_name"] == name_case["expected_user_created"], (
                f"Expected: {name_case['expected_user_created']} | Actual: {user['full_name']}\n"
            )


# ---------- Existing user ----------
def test_signup_with_existing_user(auth_headers):
    status_code, detail = create_user_with_email_already_registered(auth_headers, AUTH_SIGN_UP, role='admin')

    assert status_code == 400
    assert "already registered" in detail.lower(), (
        f"Expected 'already registered' in error, but got '{detail}'"
    )

# ---------- Role assignment tests ----------
def test_admin_role_converted_to_passenger(signup_with_custom_role):
    user = signup_with_custom_role(role="admin")
    assert user["role"] == "passenger", (
        f"Expected role 'passenger' but got '{user['role']}' when attempting to set 'admin'"
    )


# ---------- Schema tests ----------
def test_user_schema_validation(signup_with_valid_data):
    validate(instance=signup_with_valid_data, schema=user_schema)


# ---------- Login tests ----------
class TestLoginFunctionality:
    def test_admin_login(self):
        response = login(
            user=os.getenv("ADMIN_USER"),
            password=os.getenv("ADMIN_PASSWORD")
        )
        assert "access_token" in response.json()

    def test_passenger_login(self, auth_headers):
        response = login_as_passenger(auth_headers)
        assert "access_token" in response.json()

    def test_login_with_invalid_credentials(self):
        response = login(
            user=os.getenv("ADMIN_USER"),
            password="wrong_password"
        )
        assert response.status_code == 401
        assert response.json().get("detail") == "Incorrect credentials"

    def test_login_with_unregistered_user(self):
        response = login(
            user="unregistered@test.com",
            password="any_password"
        )
        assert response.status_code == 401
        assert "password" not in response.json()["detail"].lower()
        assert "email" not in response.json()["detail"].lower()
