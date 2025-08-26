# tests/auth/test_auth.py

import os
import pytest
from jsonschema import validate
from tests.auth.data import (
    emails_to_test,
    passwords_to_test,
    full_names_to_test,
    valid_password,
    valid_full_name,
)
from utils.settings import user_schema
from tests.auth.conftest import login, login_as_passenger


# ---------- Email tests ----------
class TestEmailValidation:
    @pytest.mark.parametrize("email_case", emails_to_test)
    def test_email_validation(self, signup_email_case, email_case):
        signup_email_case({
            "email": email_case["email"],
            "password": valid_password,
            "full_name": valid_full_name,
            "expected_status": email_case["expected_status"]
        })


# ---------- Password tests ----------
class TestPasswordValidation:
    @pytest.mark.parametrize("password_case", passwords_to_test)
    def test_password_validation(self, signup_password_case, password_case):
        signup_password_case({
            "password": password_case["password"],
            "full_name": valid_full_name,
            "expected_status": password_case["expected_status"]
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


# ---------- Role assignment tests ----------
def test_admin_role_converted_to_passenger(self, signup_with_custom_role):
    user = signup_with_custom_role(role="admin")
    assert user["role"] == "passenger", (
        f"Expected role 'passenger' but got '{user['role']}' when attempting to set 'admin'"
    )


# ---------- Schema tests ----------
def test_user_schema_validation(self, signup_with_valid_data):
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