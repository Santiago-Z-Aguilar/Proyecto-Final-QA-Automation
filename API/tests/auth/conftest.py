# tests/auth/conftest.py

import logging
from typing import Any, Dict, Optional, Tuple
import pytest

from API.utils.data import valid_password, valid_full_name
from API.utils.api_helpers import api_request
from API.utils.settings import AUTH_LOGIN, AUTH_SIGN_UP
from API.utils.user_helpers import (
    get_unique_email,
    get_user_by_email,
    delete_user_by_id,
    user_exist_skip,
    _create_user,
    _build_user_data,
    _extract_user_id_from_response,
)

logger = logging.getLogger("qa_tests")


def _assert_created_user_status(resp, expected_status: int, context: Dict[str, Any]) -> None:
    """Assert response status equals expected_status, with helpful logs on mismatch."""
    assert resp is not None, "API response is None"
    if resp.status_code != expected_status:
        logger.error(
            "Signup status mismatch | expected=%s actual=%s | context=%s | response_text=%s",
            expected_status, resp.status_code, context, getattr(resp, "text", "<no text>")
        )
    assert resp.status_code == expected_status, (
        f"\n---\nTest failed for {context}\n"
        f"Expected: {expected_status} | Actual: {resp.status_code}\n"
        f"Response: {getattr(resp, 'text', '<no text>')}\n---"
    )

def _signup_case(case: Dict[str, Any], auth_headers, prefix: str):
    """
    Run signup and return (response, expected_status, user_or_none).
    """
    email = case.get("email", get_unique_email(prefix=prefix))
    password = case.get("password", valid_password)
    full_name = case.get("full_name", valid_full_name)
    expected_status = case["expected_status"]

    try:
        existing = get_user_by_email(email, auth_headers)
        if existing and existing.get("id"):
            delete_user_by_id(existing["id"], auth_headers)
    except Exception:
        pass

    payload = _build_user_data(email, password, full_name)
    created_id = None
    user = None

    try:
        resp = _create_user(
            payload,
            auth_headers,
            path=AUTH_SIGN_UP,
            treat_duplicate_as_success=(expected_status == 201),
        )
        if resp.status_code == 201:
            created_id = _extract_user_id_from_response(resp)
            user = get_user_by_email(email, auth_headers) or {}
        return resp, expected_status, user
    finally:
        try:
            if created_id:
                delete_user_by_id(created_id, auth_headers)
            else:
                found = get_user_by_email(email, auth_headers)
                if found and found.get("id"):
                    delete_user_by_id(found["id"], auth_headers)
        except Exception:
            pass

@pytest.fixture
def signup_email_case(auth_headers):
    """Fixture to test email validations (strict expected_status)."""
    def _signup_email(case: Dict[str, Any]):
        return _signup_case(case, auth_headers, prefix="emailtest_jasy")
    return _signup_email


@pytest.fixture
def signup_password_case(auth_headers):
    """Fixture to test password validations (strict expected_status)."""
    def _signup_password(case: Dict[str, Any]):
        return _signup_case(case, auth_headers, prefix="pwtest_jasy")
    return _signup_password


@pytest.fixture
def signup_full_name_case(auth_headers):
    """Fixture to test full_name validations (strict expected_status)."""
    def _signup_fullname(case: Dict[str, Any]):
        return _signup_case(case, auth_headers, prefix="nametest_jasy")
    return _signup_fullname


@pytest.fixture
def signup_with_custom_role(auth_headers):
    """
    Create a user with a custom role (expects success).
    Returns the created user object; cleanup by ID is guaranteed.
    """
    def _signup(role: str, prefix: str = "role_test_jasy"):
        test_email = get_unique_email(prefix="custom_role_jasy")
        data = _build_user_data(test_email, valid_password, valid_full_name, role=role)

        created_id: Optional[str] = None
        try:
            resp = _create_user(data, auth_headers, path=AUTH_SIGN_UP, treat_duplicate_as_success=True)
            created_id = _extract_user_id_from_response(resp)
            user = get_user_by_email(test_email, auth_headers) or {}
            return user
        finally:
            try:
                if created_id:
                    delete_user_by_id(created_id, auth_headers)
                else:
                    found = get_user_by_email(test_email, auth_headers)
                    if found and found.get("id"):
                        delete_user_by_id(found["id"], auth_headers)
            except Exception as e:
                logger.warning("Cleanup exception for '%s': %s", test_email, e)
    return _signup


@pytest.fixture
def signup_with_valid_data(auth_headers):
    """
    Create a valid user and yield its object.
    Ensures cleanup by ID; falls back to email lookup if needed.
    """
    unique_email = get_unique_email(prefix="valid_user_jasy")
    data = _build_user_data(unique_email, valid_password, valid_full_name)

    user_exist_skip(unique_email, auth_headers)
    created_id: Optional[str] = None
    try:
        resp = _create_user(data, auth_headers, path=AUTH_SIGN_UP, treat_duplicate_as_success=True)
        created_id = _extract_user_id_from_response(resp)
        user = get_user_by_email(unique_email, auth_headers) or {}
        yield user
    finally:
        try:
            if created_id:
                delete_user_by_id(created_id, auth_headers)
            else:
                found = get_user_by_email(unique_email, auth_headers)
                if found and found.get("id"):
                    delete_user_by_id(found["id"], auth_headers)
        except Exception as e:
            logger.warning("Cleanup exception for '%s': %s", unique_email, e)


def login(user: str, password: str):
    """Perform login and return the raw response. Only 200 and 401 are expected."""
    response = api_request("post", AUTH_LOGIN, data={"username": user, "password": password})
    if response is None:
        raise Exception("Login failed after retries")
    if response.status_code not in (200, 401):
        raise Exception(f"Unexpected status: {response.status_code}. Response: {response.text}")
    return response


def login_as_passenger(auth_headers):
    """
    Create a passenger user, assert role from read, then perform login.
    Ensures cleanup by ID; falls back to email lookup if needed.
    """
    unique_email = get_unique_email(prefix="passenger_test_jasy")
    data = _build_user_data(unique_email, valid_password, valid_full_name)

    created_id: Optional[str] = None
    try:
        resp = _create_user(data, auth_headers, path=AUTH_SIGN_UP, treat_duplicate_as_success=True)
        created_id = _extract_user_id_from_response(resp)

        user = get_user_by_email(unique_email, auth_headers)
        assert user and user.get("role") == "passenger"

        return login(unique_email, valid_password)
    finally:
        try:
            if created_id:
                delete_user_by_id(created_id, auth_headers)
            else:
                found = get_user_by_email(unique_email, auth_headers)
                if found and found.get("id"):
                    delete_user_by_id(found["id"], auth_headers)
        except Exception as e:
            logger.warning("Cleanup exception for '%s': %s", unique_email, e)
