# tests/auth/conftest

import logging
from typing import Any, Dict, Optional, Tuple
from uuid import uuid4

import pytest

from tests.auth.data import valid_password, valid_full_name
from utils.api_helpers import api_request
from utils.settings import AUTH_LOGIN
from utils.user_helpers import (
    get_user_by_email,
    delete_user_by_email,
    user_exist_skip,
    _create_user,
    get_unique_email,
)

# Centralized logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qa_tests")


# ---------- Shared helpers ----------
def _build_data(email: str, password: str, full_name: str, role: Optional[str] = None) -> Dict[str, Any]:
    """Builds the request body for user creation."""
    data: Dict[str, Any] = {
        "email": email,
        "password": password,
        "full_name": full_name
    }
    if role is not None:
        data["role"] = role
    return data


def _assert_status(resp, expected_status: int, context: Dict[str, Any]) -> None:
    """Ensures that the status code matches the expected one."""
    assert resp is not None, "API response is None"
    assert resp.status_code == expected_status, (
        f"\n---\nTest failed for {context}\n"
        f"Expected: {expected_status} | Actual: {resp.status_code}\n"
        f"Response: {getattr(resp, 'text', '<no text>')}\n---"
    )


def _cleanup_if_created(email: str, auth_headers: Dict[str, str], resp) -> None:
    """Deletes the user only if it was successfully created (201)."""
    if resp and resp.status_code == 201:
        try:
            deleted = delete_user_by_email(email, auth_headers)
            logger.info(f"Cleanup: {'✅' if deleted else '❌'} User '{email}' deleted")
        except Exception as e:
            logger.warning(f"Cleanup exception for '{email}': {e}")


def _unique_email(prefix: str = "t") -> str:
    """Generates a unique email."""
    try:
        return get_unique_email(prefix=prefix)
    except Exception:
        return f"{prefix}_{uuid4().hex}@example.com"


# ---------- Fixtures ----------
@pytest.fixture
def signup_test_case(auth_headers):
    """Fixture to execute signup test cases with automatic cleanup."""

    def _signup(case: Dict[str, Any]) -> Tuple[Any, str, Optional[Dict[str, Any]]]:
        email = case.get("email", _unique_email())
        password = case.get("password", valid_password)
        full_name = case.get("full_name", valid_full_name)
        expected_status = case["expected_status"]

        user_exist_skip(email, auth_headers)
        data = _build_data(email, password, full_name)

        resp = None
        try:
            resp = _create_user(data, auth_headers)
            _assert_status(resp, expected_status, case)

            user = get_user_by_email(email, auth_headers) if resp.status_code == 201 else None
            return resp, email, user
        finally:
            _cleanup_if_created(email, auth_headers, resp)

    return _signup


@pytest.fixture
def signup_with_custom_role(auth_headers):
    """Fixture to create users with custom roles (without validation)."""
    def _signup(role: str, prefix: str = "role_test"):
        test_email = _unique_email(prefix=prefix)
        data = _build_data(test_email, valid_password, valid_full_name, role=role)

        resp = None
        try:
            resp = _create_user(data, auth_headers)
            _assert_status(resp, 201, {"attempted_role": role})  # Solo verifica que se creó
            return get_user_by_email(test_email, auth_headers)  # Retorna el usuario SIN validar
        finally:
            _cleanup_if_created(test_email, auth_headers, resp)
    return _signup


@pytest.fixture
def signup_with_valid_data(auth_headers):
    """Fixture to create a valid user with automatic cleanup."""
    unique_email = _unique_email(prefix="valid_user")
    data = _build_data(unique_email, valid_password, valid_full_name)

    user_exist_skip(unique_email, auth_headers)
    resp = None

    try:
        resp = _create_user(data, auth_headers)
        _assert_status(resp, 201, data)

        user = get_user_by_email(unique_email, auth_headers)
        yield user
    finally:
        _cleanup_if_created(unique_email, auth_headers, resp)


# ---------- Authentication helpers ----------
def login(user: str, password: str):
    """Performs login and returns the full response."""
    response = api_request("post", AUTH_LOGIN, data={"username": user, "password": password})
    if response is None:
        raise Exception("Login failed after retries")
    if response.status_code not in (200, 401):
        raise Exception(f"Unexpected status: {response.status_code}, Response: {response.text}")
    return response


def login_as_passenger(auth_headers):
    """Creates a passenger user and performs login."""
    unique_email = _unique_email(prefix="passenger_test")
    data = _build_data(unique_email, valid_password, valid_full_name)

    resp = None
    try:
        resp = _create_user(data, auth_headers)
        _assert_status(resp, 201, data)

        user = get_user_by_email(unique_email, auth_headers)
        assert user["role"] == "passenger"

        return login(unique_email, valid_password)
    finally:
        _cleanup_if_created(unique_email, auth_headers, resp)
