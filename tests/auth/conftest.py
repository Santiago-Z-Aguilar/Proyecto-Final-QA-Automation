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

# Configure logging once (idempotent)
logger = logging.getLogger("qa_tests")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)


# ---------- Small shared helpers ----------

def _build_data(email: str, password: str, full_name: str, role: Optional[str] = None) -> Dict[str, Any]:
    """Build the request body for user creation."""
    data: Dict[str, Any] = {"email": email, "password": password, "full_name": full_name}
    if role is not None:
        data["role"] = role
    return data


def _assert_status(
    resp,
    expected_status: int,
    variable: str,
    variable_value: Any,
    data: Dict[str, Any],
) -> None:
    """Assert that the API response matches the expected status code."""
    assert resp is not None, "API response is None"
    assert resp.status_code == expected_status, (
        f"\n---\nTest failed for {variable}: {variable_value}\n"
        f"Data: {data}\n"
        f"Expected: {expected_status} | Actual: {resp.status_code}\n"
        f"Response: {getattr(resp, 'text', '<no text>')}\n---"
    )


def _cleanup_if_created(email: str, auth_headers: Dict[str, str], resp) -> None:
    """Delete the user only if it was successfully created (201)."""
    if resp and resp.status_code == 201:
        try:
            deleted = delete_user_by_email(email, auth_headers)
        except Exception as e:
            deleted = False
            logger.warning(f"Cleanup exception for '{email}': {e}")
        status = "✅" if deleted else "❌"
        logger.info(f"Cleanup: {status} User '{email}' deleted.")


def _unique_email(prefix: str = "t") -> str:
    """Generate a unique email, preferring get_unique_email if available."""
    try:
        return get_unique_email(prefix=prefix)
    except Exception:
        return f"{prefix}_{uuid4().hex}@example.com"


# ---------- Fixtures ----------

@pytest.fixture
def signup_test_case(auth_headers):
    """
    Execute a signup test case with automatic cleanup only if user is created (201).
    Returns (resp, email, user_or_none). Keeps behavior and validations intact.
    """
    def _signup(case: Dict[str, Any], variable: str = "email") -> Tuple[Any, str, Optional[Dict[str, Any]]]:
        email = case.get("email")
        password = case.get("password", valid_password)
        full_name = case.get("full_name", valid_full_name)
        expected_status = case["expected_status"]

        # Initial check - skip if user exists
        user_exist_skip(email, auth_headers)

        data = _build_data(email, password, full_name)
        resp = None
        try:
            resp = _create_user(data, auth_headers)
            _assert_status(resp, expected_status, variable, case.get(variable), data)

            user = None
            if resp.status_code == 201:
                user = get_user_by_email(email, auth_headers)
            return resp, email, user
        finally:
            _cleanup_if_created(email, auth_headers, resp)

    return _signup


@pytest.fixture()
def signup_with_custom_role(auth_headers):
    """
    Create a user with a custom role and verify the system sets it to 'passenger'.
    Returns the created user object. Behavior identical to your version.
    """
    def _signup(role: str):
        test_email = _unique_email(prefix="role_test")
        data = _build_data(test_email, valid_password, valid_full_name, role=role)

        resp = None
        try:
            resp = _create_user(data, auth_headers)
            assert resp is not None, "API response is None"
            assert resp.status_code == 201, "User creation failed"

            created_user = get_user_by_email(test_email, auth_headers)
            assert created_user is not None, "User not found after creation"
            assert created_user["role"] == "passenger"

            return created_user
        finally:
            _cleanup_if_created(test_email, auth_headers, resp)

    return _signup


@pytest.fixture()
def signup_with_valid_data(auth_headers):
    """
    Create a valid user, yield the user object, and clean it up afterwards.
    """
    unique_email = _unique_email(prefix="pwtest")
    data = _build_data(unique_email, valid_password, valid_full_name)

    user_exist_skip(unique_email, auth_headers)

    resp = None
    try:
        resp = _create_user(data, auth_headers)
        assert resp is not None, "API response is None"
        assert resp.status_code == 201

        user = get_user_by_email(unique_email, auth_headers)
        assert user is not None

        yield user
    finally:
        _cleanup_if_created(unique_email, auth_headers, resp)


# ---------- Auth helpers ----------

def login(user: str, password: str):
    """
    Send a login request and return the full response object for further assertions.
    Valid statuses: 200 or 401. Keeps same behavior and checks.
    """
    response = api_request("post", AUTH_LOGIN, data={"username": user, "password": password})
    if response is None:
        raise Exception("❌ Login failed after some retries")
    if response.status_code not in (200, 401):
        raise Exception(f"❌ Unexpected status code: {response.status_code}, Response: {response.text}")
    return response


def login_as_passenger(auth_headers):
    """
    Create a passenger user, log in, and clean up the created user.
    Returns the login response object.
    """
    unique_email = _unique_email(prefix="passenger_test")
    data = _build_data(unique_email, valid_password, valid_full_name)

    resp = None
    try:
        resp = _create_user(data, auth_headers)
        assert resp and resp.status_code == 201

        user = get_user_by_email(unique_email, auth_headers)
        assert user and user["role"] == "passenger"

        token_data = login(unique_email, valid_password)
        return token_data
    finally:
        _cleanup_if_created(unique_email, auth_headers, resp)
