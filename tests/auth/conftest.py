# tests/auth/conftest.py

import pytest
import logging
from utils.api_helpers import api_request
from utils.user_helpers import get_user_by_email, delete_user_by_email
from utils.settings import AUTH_SIGN_UP, USERS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qa_tests")


def _verify_user_not_exists(email, auth_headers):
    """Check if user already exists and skip test if true."""
    existing_user = get_user_by_email(email, auth_headers)
    if existing_user:
        pytest.skip(f"User '{email}' already exists in database. Test skipped.")


def _handle_signup_retry(payload, auth_headers, max_retries=3):
    """
    Execute signup with retry logic for specific error cases.
    Returns API response object.
    """
    email = payload["email"]

    for attempt in range(1, max_retries + 1):
        resp = api_request("post", AUTH_SIGN_UP, json=payload)

        # # Handle known bug: 500 when user already exists
        # if resp.status_code == 500 and "already registered" in resp.text.lower():
        #     logger.error(f"⚠️ Detected bug: 500 and then 400 (duplicate user)")
        #     return resp  # Return the 500 response as bug evidence

        # Expected case: User already registered (400)
        if resp.status_code == 400 and "already registered" in resp.text.lower():
            logger.warning(f"Duplicate user (attempt {attempt}/{max_retries})")
            if attempt < max_retries:
                deleted = delete_user_by_email(email, auth_headers)
                if not deleted:
                    logger.error(f"Failed to delete {email} for retry")
                    break
            continue

        # For non-duplicate errors, exit retry loop
        break

    return resp


@pytest.fixture
def signup_test_case(auth_headers):
    def _signup(case, variable="email"):
        """
        Execute signup test case with automatic cleanup.
        Returns tuple: (response, email, user_data) if successful.
        """
        email = case.get("email")
        password = case.get("password")
        full_name = case.get("full_name")

        # Initial check - skip if user exists
        _verify_user_not_exists(email, auth_headers)

        payload = {
            "email": email,
            "password": password,
            "full_name": full_name
        }

        try:
            # Execute signup with retry logic
            resp = _handle_signup_retry(payload, auth_headers)

            # Validate response
            assert resp is not None, "API response is None"
            assert resp.status_code == case["expected_status"], (
                f"\n---\nTest failed for {variable}: {case.get(variable)}\n"
                f"Payload: {payload}\n"
                f"Expected: {case['expected_status']} | Actual: {resp.status_code}\n"
                f"Response: {resp.text}\n---"
            )

            # Return user data if created successfully
            user = None
            if resp.status_code == 201:
                user = get_user_by_email(email, auth_headers)
            return resp, email, user

        finally:
            # Cleanup only users created in this test
            if resp and resp.status_code == 201:
                deleted = delete_user_by_email(email, auth_headers)
                status = "✅" if deleted else "❌"
                logger.info(f"Cleanup: {status} User '{email}' deleted.")

    return _signup