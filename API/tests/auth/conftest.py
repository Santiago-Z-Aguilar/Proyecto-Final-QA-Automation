# tests/auth/conftest.py

import logging
from typing import Any, Dict, Optional, Tuple
import pytest

from API.utils.data import valid_password, valid_full_name
from API.utils.api_helpers import api_request
from API.utils.settings import AUTH_LOGIN
from API.utils.user_helpers import (
    get_unique_email,
    get_user_by_email,
    delete_user_by_email,
    user_exist_skip,
    _create_user,
)

# ---------- Logging ----------
# NOTE: pytest already manages logging. Avoid basicConfig unless you need custom setup.
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qa_tests")


# ---------- Helpers ----------

def _build_data(email: str, password: str, full_name: str, role: Optional[str] = None) -> Dict[str, Any]:
    """Builds user creation payload."""
    data = {"email": email, "password": password, "full_name": full_name}
    if role is not None:
        data["role"] = role
    return data


def _assert_created_user_status(resp, expected_status: int, context: Dict[str, Any]) -> None:
    """
    Asserts the expected status code and logs a clear error message on failure.
    This guarantees we get a log line whenever the assertion fails.
    """
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


def _signup_case(case: Dict[str, Any], auth_headers, prefix: str) -> Tuple[Any, str, Optional[Dict[str, Any]]]:
    """
    Common signup flow for field validation tests.
    - Skips if expecting 201 and user already exists.
    - Calls _create_user with duplicate-as-success only for expected 201.
    - Performs hybrid cleanup if a user exists after the call.
    """
    email = case.get("email", get_unique_email(prefix=prefix))
    password = case.get("password", valid_password)
    full_name = case.get("full_name", valid_full_name)
    expected_status = case["expected_status"]

    if expected_status == 201:
        user_exist_skip(email, auth_headers)

    data = _build_data(email, password, full_name)

    resp = None
    user = None
    try:
        resp = _create_user(
            data,
            auth_headers,
            treat_duplicate_as_success=(expected_status == 201)
        )
        _assert_created_user_status(resp, expected_status, case)

        if resp.status_code == 201:
            user = get_user_by_email(email, auth_headers)

        return resp, email, user

    except Exception:
        # This ensures 500s (or any unexpected exception) are also logged with full traceback.
        logger.exception(
            "Unexpected exception during signup | email=%s | expected_status=%s | case=%s",
            email, expected_status, case
        )
        raise

    finally:
        try:
            existing_user = user or get_user_by_email(email, auth_headers)
            if existing_user:
                deleted = delete_user_by_email(email, auth_headers)
                logger.info("Cleanup: %s User '%s' deleted", "✅" if deleted else "❌", email)
        except Exception as e:
            logger.warning("Cleanup exception for '%s': %s", email, e)


# ---------- Fixtures by field ----------
@pytest.fixture
def signup_email_case(auth_headers):
    """Fixture to test email validations."""
    def _signup_email(case: Dict[str, Any]):
        return _signup_case(case, auth_headers, prefix="emailtest_jasy")
    return _signup_email

@pytest.fixture
def signup_password_case(auth_headers):
    """Fixture to test password validations."""
    def _signup_password(case: Dict[str, Any]):
        return _signup_case(case, auth_headers, prefix="pwtest_jasy")
    return _signup_password

@pytest.fixture
def signup_full_name_case(auth_headers):
    """Fixture to test full_name validations."""
    def _signup_fullname(case: Dict[str, Any]):
        return _signup_case(case, auth_headers, prefix="nametest_jasy")
    return _signup_fullname


# ---------- Other fixtures ----------
@pytest.fixture
def signup_with_custom_role(auth_headers):
    """Fixture to create users with custom role (always expects success)."""
    def _signup(role: str, prefix: str = "role_test_jasy"):
        test_email = get_unique_email(prefix)
        data = _build_data(test_email, valid_password, valid_full_name, role=role)

        resp = None
        try:
            resp = _create_user(data, auth_headers, treat_duplicate_as_success=True)
            _assert_created_user_status(resp, 201, {"attempted_role": role})
            return get_user_by_email(test_email, auth_headers)
        finally:
            try:
                existing_user = get_user_by_email(test_email, auth_headers) is not None
                if existing_user:
                    deleted = delete_user_by_email(test_email, auth_headers)
                    logger.info(f"Cleanup: {'✅' if deleted else '❌'} User '{test_email}' deleted")
            except Exception as e:
                logger.warning(f"Cleanup exception for '{test_email}': {e}")
    return _signup

@pytest.fixture
def signup_with_valid_data(auth_headers):
    """Fixture to create a valid user and yield its object, with auto cleanup."""
    unique_email = get_unique_email(prefix="valid_user_jasy")
    data = _build_data(unique_email, valid_password, valid_full_name)

    user_exist_skip(unique_email, auth_headers)
    resp = None
    try:
        resp = _create_user(data, auth_headers, treat_duplicate_as_success=True)
        _assert_created_user_status(resp, 201, data)
        user = get_user_by_email(unique_email, auth_headers)
        yield user
    finally:
        try:
            existing_user = get_user_by_email(unique_email, auth_headers) is not None
            if existing_user:
                deleted = delete_user_by_email(unique_email, auth_headers)
                logger.info(f"Cleanup: {'✅' if deleted else '❌'} User '{unique_email}' deleted")
        except Exception as e:
            logger.warning(f"Cleanup exception for '{unique_email}': {e}")


# ---------- Authentication helpers ----------
def login(user: str, password: str):
    """Performs login and returns the raw response. Only 200 and 401 are expected."""
    response = api_request("post", AUTH_LOGIN, data={"username": user, "password": password})
    if response is None:
        raise Exception("Login failed after retries")
    if response.status_code not in (200, 401):
        raise Exception(f"Unexpected status: {response.status_code}, Response: {response.text}")
    return response

def login_as_passenger(auth_headers):
    """Creates a passenger user and logs in. Ensures role is 'passenger'."""
    unique_email = get_unique_email(prefix="passenger_test_jasy")
    data = _build_data(unique_email, valid_password, valid_full_name)

    resp = None
    try:
        resp = _create_user(data, auth_headers, treat_duplicate_as_success=True)
        _assert_created_user_status(resp, 201, data)

        user = get_user_by_email(unique_email, auth_headers)
        assert user and user.get("role") == "passenger"

        return login(unique_email, valid_password)
    finally:
        try:
            existing_user = get_user_by_email(unique_email, auth_headers) is not None
            if existing_user:
                deleted = delete_user_by_email(unique_email, auth_headers)
                logger.info(f"Cleanup: {'✅' if deleted else '❌'} User '{unique_email}' deleted")
        except Exception as e:
            logger.warning(f"Cleanup exception for '{unique_email}': {e}")
