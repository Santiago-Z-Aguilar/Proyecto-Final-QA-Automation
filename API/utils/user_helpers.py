# utils/user_helpers.py

import logging
from uuid import uuid4
from typing import Dict, Optional, Any
from requests.models import Response
from time import sleep
import json
import pytest

from API.utils.api_helpers import api_request
from API.utils.data import valid_password, valid_full_name
from API.utils.settings import USERS, AUTH_SIGN_UP

logger = logging.getLogger("qa_tests")

# Tuning constants
DEFAULT_RETRIES = 5
CLEANUP_DELAY = 1


def get_unique_email(prefix: str = "test") -> str:
    """Return a unique email address for testing."""
    return f"{prefix}_{uuid4().hex}@example.com"


def _build_user_data(
    email: Optional[str] = None,
    password: Optional[str] = None,
    full_name: Optional[str] = None,
    role: Optional[str] = None,
    *,
    default_prefix: str = "user",  # kept for API compatibility if someday needed
) -> dict:
    """
    Build a user payload including only fields that are not None.
    Passing an empty string ("") is a valid explicit value.
    """
    payload: Dict[str, Any] = {}
    if email is not None:
        payload["email"] = email
    if password is not None:
        payload["password"] = password
    if full_name is not None:
        payload["full_name"] = full_name
    if role is not None:
        payload["role"] = role
    return payload


def get_user_by_email(email: str, auth_headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    Return the user object that matches the given email by paging /users.
    Returns None if not found or on non-200 responses.
    """
    PAGE = 50
    skip = 0
    while True:
        resp = api_request("get", USERS, headers=auth_headers, params={"skip": skip, "limit": PAGE})
        if resp is None or resp.status_code != 200:
            return None

        try:
            batch = resp.json()
        except Exception:
            return None

        if not batch:
            return None

        for u in batch:
            if u.get("email") == email:
                return u

        if len(batch) < PAGE:
            return None
        skip += PAGE


def user_exist_skip(email: str, auth_headers: Dict[str, str]) -> None:
    """Skip the test if the given email already exists in the database."""
    existing_user = get_user_by_email(email, auth_headers)
    if existing_user:
        pytest.skip(f"User '{email}' already exists in database. Test skipped.")


def _extract_user_id_from_response(resp: Response) -> Optional[str]:
    """Try to extract 'id' from a JSON response body."""
    try:
        data = resp.json() if getattr(resp, "content", None) else {}
        return data.get("id")
    except Exception:
        return None


def _create_user(
    payload: Dict[str, Any],
    auth_headers: Optional[Dict[str, str]] = None,
    path: Optional[str] = None,
    max_retries: int = DEFAULT_RETRIES,
    treat_duplicate_as_success: bool = True,
) -> Response:
    """
    Create a user with duplicate resilience.

    Behavior:
      - If 'email' is not in payload or is None: just POST (no duplicate handling).
      - On 201: return response as-is.
      - On 400 with "already registered" semantics:
          * If the user exists:
              - If treat_duplicate_as_success=True → return a synthetic 201 with the real user id.
              - Else → return the real 400 response.
          * If not found → retry up to max_retries.
      - Any other status → return as-is.

    5xx/timeouts are handled by api_request’s internal logic (e.g., retries).
    """
    path = path or USERS

    if "email" not in payload or payload.get("email") is None:
        return api_request("post", path, json=payload, headers=auth_headers)

    email = payload["email"]
    last_resp: Optional[Response] = None

    for _ in range(1, max_retries + 1):
        resp = api_request("post", path, json=payload, headers=auth_headers)
        last_resp = resp

        if resp is None:
            continue

        if resp.status_code == 201:
            return resp

        # Duplicate handling (message wording may vary; match loosely).
        if resp.status_code == 400 and "already" in resp.text.lower() and "register" in resp.text.lower():
            logger.warning("User already registered; fetching existing user to synthesize 201.")
            existing_user = get_user_by_email(email, auth_headers)
            if existing_user:
                if treat_duplicate_as_success:
                    fake = Response()
                    fake.status_code = 201
                    fake._content = json.dumps({
                        "message": "user_already_exists",
                        "email": email,
                        "role": existing_user.get("role") or payload.get("role"),
                        "id": existing_user.get("id"),
                    }).encode("utf-8")
                    fake.headers["Content-Type"] = "application/json"
                    fake.encoding = "utf-8"
                    return fake
                return resp
            continue

        return resp

    return last_resp  # best effort


def create_user_with_email_already_registered(
    auth_headers: Dict[str, str],
    ENDPOINT: str,
    role: Optional[str],
):
    """
    Create a user, then try to create it again to capture the duplicate error.
    Returns (status_code, detail_text). Ensures cleanup by ID when possible.
    """
    unique_email = get_unique_email(prefix="registered_jasy")
    payload = _build_user_data(email=unique_email, password=valid_password, full_name=valid_full_name, role=role)

    created_id: Optional[str] = None
    try:
        first = _create_user(payload, auth_headers, path=ENDPOINT, treat_duplicate_as_success=True)
        created_id = _extract_user_id_from_response(first)

        exist = _create_user(payload, auth_headers, path=ENDPOINT, treat_duplicate_as_success=False)
        data = exist.json()
        return exist.status_code, data.get("detail")
    finally:
        if created_id:
            delete_user_by_id(created_id, auth_headers)
        else:
            user = get_user_by_email(unique_email, auth_headers)
            if user and user.get("id"):
                delete_user_by_id(user["id"], auth_headers)


def delete_user_by_email(email: str, auth_headers: Dict[str, str]) -> bool:
    """
    Deprecated: Prefer delete_user_by_id whenever possible.
    Kept as fallback for endpoints that do not expose the user ID.
    """
    user = get_user_by_email(email, auth_headers)
    if not user:
        return False
    return delete_user_by_id(user["id"], auth_headers)


def delete_user_by_id(user_id: str, auth_headers: Dict[str, str]) -> bool:
    """Delete a user by ID. Returns True on 204, False otherwise."""
    resp = api_request("delete", f"{USERS.rstrip('/')}/{user_id}", headers=auth_headers)
    if resp and resp.status_code == 204:
        logger.info(f"Deleted user id '{user_id}'")
        sleep(CLEANUP_DELAY)
        return True
    status = getattr(resp, "status_code", "<no resp>")
    text = getattr(resp, "text", "<no text>")
    logger.error(f"User not deleted by id '{user_id}'. Status: {status}. Response: {text}")
    return False

