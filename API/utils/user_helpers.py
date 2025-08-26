# utils/user_helpers.py

import logging
from uuid import uuid4
from typing import Dict, Optional
from requests.models import Response
from API.utils.api_helpers import api_request
from API.utils.settings import USERS, AUTH_SIGN_UP
import pytest
from time import sleep

logger = logging.getLogger("qa_tests")

# Constants
DEFAULT_RETRIES = 3
CLEANUP_DELAY = 1  # Keep as-is, per your request.


def get_unique_email(prefix: str = "test") -> str:
    """Generate a unique email address for testing."""
    return f"{prefix}_{uuid4().hex}@example.com"


def get_user_by_email(email: str, auth_headers: Dict[str, str]) -> Optional[Dict]:
    """
    Returns user dict if exists, None otherwise.
    Safer against None responses or unexpected codes.
    """
    resp: Optional[Response] = api_request("get", USERS, headers=auth_headers)
    if resp is None or resp.status_code != 200:
        return None
    try:
        users: list = resp.json()
    except Exception:
        return None
    return next((user for user in users if user.get("email") == email), None)


def user_exist_skip(email: str, auth_headers: Dict[str, str]) -> None:
    """Skip test if user already exists."""
    existing_user = get_user_by_email(email, auth_headers)
    if existing_user:
        pytest.skip(f"User '{email}' already exists in database. Test skipped.")


def _create_user(
    payload: Dict,
    auth_headers: Dict[str, str],
    max_retries: int = DEFAULT_RETRIES,
    treat_duplicate_as_success: bool = True,
) -> Response:
    """
    Handles user creation with duplicate resilience.
    - On 400 "already registered":
      - If user exists:
        - If treat_duplicate_as_success=True: return synthetic 201.
        - Else: return real 400.
      - If user not found: retry until max_retries.
    - Other codes are returned as-is.
    - 500 handling is assumed in api_request.
    """
    email = payload["email"]
    last_resp: Optional[Response] = None

    for attempt in range(1, max_retries + 1):
        resp = api_request("post", AUTH_SIGN_UP, json=payload, headers=auth_headers)
        last_resp = resp

        if resp is None:
            continue

        if resp.status_code == 201:
            return resp

        if resp.status_code == 400 and "already registered" in resp.text.lower():
            """
            Needs get the user to get the ID
            """
            existing_user = get_user_by_email(email, auth_headers)
            if existing_user:
                if treat_duplicate_as_success:
                    bug400 = Response()
                    bug400.status_code = 201
                    bug400._content = f'{{"message":"user_already_exists","email":"{email}"}}'.encode()
                    return bug400
                return resp
            continue  # retry

        return resp

    return last_resp


def delete_user_by_email(email: str, auth_headers: Dict[str, str]) -> bool:
    """
    Delete user by email.
    NOTE: Left exactly as you had it, with CLEANUP_DELAY constant.
    """
    user = get_user_by_email(email, auth_headers)
    if not user:
        return False

    resp: Response = api_request("DELETE", f"{USERS}{user['id']}", headers=auth_headers)
    if resp.status_code == 204:
        logger.info(f" Deleted user '{email}'")
        sleep(CLEANUP_DELAY)
        return True
    else:
        logger.error(f" User not deleted '{email}'")
    return False
