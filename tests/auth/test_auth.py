# tests/auth/test_auth

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
from tests.auth.conftest import _unique_email, login, login_as_passenger


class TestEmailValidation:
    @pytest.mark.parametrize("email_case", emails_to_test)
    def test_email_validation(self, signup_test_case, email_case):
        """Validation tests for different email formats."""
        signup_test_case({
            "email": email_case["email"],
            "password": valid_password,
            "full_name": valid_full_name,
            "expected_status": email_case["expected_status"]
        })


class TestPasswordValidation:
    @pytest.mark.parametrize("password_case", passwords_to_test)
    def test_password_validation(self, signup_test_case, password_case):
        """Validation tests for different password formats."""
        signup_test_case({
            "email": _unique_email(prefix="test_password"),
            "password": password_case["password"],
            "full_name": valid_full_name,
            "expected_status": password_case["expected_status"]
        })


class TestFullNameValidation:
    @pytest.mark.parametrize("name_case", full_names_to_test)
    def test_name_validation(self, signup_test_case, name_case):
        """Validation and normalization tests for full names."""
        case_data = {
            "email": _unique_email(prefix="test_full_name"),
            "full_name": name_case["full_name"],
            "expected_status": name_case["expected_status"]
        }
        # Solo agregar password si es diferente del default
        if "password" in name_case:
            case_data["password"] = name_case["password"]

        resp, email, user = signup_test_case(case_data)

        if name_case["expected_status"] == 201 and "expected_user_created" in name_case:
            assert user["full_name"] == name_case["expected_user_created"]

class TestRoleAssignment:
    def test_admin_role_converted_to_passenger(self, signup_with_custom_role):
        """Verify that role='admin' is forced to 'passenger'."""
        user = signup_with_custom_role(role="admin")
        assert user["role"] == "passenger", (
            f"Expected role 'passenger' but got '{user['role']}' when attempting to set 'admin'"
        )


class TestUserSchema:
    def test_user_schema_validation(self, signup_with_valid_data):
        """Ensures that the created user matches the expected schema."""
        validate(instance=signup_with_valid_data, schema=user_schema)


class TestLoginFunctionality:
    def test_admin_login(self):
        """Successful login test as administrator."""
        response = login(
            user=os.getenv("ADMIN_USER"),
            password=os.getenv("ADMIN_PASSWORD")
        )
        assert "access_token" in response.json()

    def test_passenger_login(self, auth_headers):
        """Successful login test as passenger."""
        response = login_as_passenger(auth_headers)
        assert "access_token" in response.json()

    def test_login_with_invalid_credentials(self):
        """Login test with incorrect credentials."""
        response = login(
            user=os.getenv("ADMIN_USER"),
            password="wrong_password"
        )
        assert response.status_code == 401
        assert response.json().get("detail") == "Incorrect credentials"

    def test_login_with_unregistered_user(self):
        """Login test with unregistered user."""
        response = login(
            user="unregistered@test.com",
            password="any_password"
        )
        assert response.status_code == 401
        assert "credentials" in response.json()["detail"].lower()
