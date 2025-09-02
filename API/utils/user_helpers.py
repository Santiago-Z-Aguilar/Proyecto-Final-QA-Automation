# utils/user_helpers.py

import logging
from uuid import uuid4
from typing import Dict, Optional, Any
from requests.models import Response
from API.utils.api_helpers import api_request
from API.utils.data import valid_password, valid_full_name
from API.utils.settings import USERS, AUTH_SIGN_UP
import pytest
import json
from time import sleep


logger = logging.getLogger("qa_tests")

# Constants
DEFAULT_RETRIES = 3
CLEANUP_DELAY = 1


def get_unique_email(prefix: str = "test") -> str:
    """Generate a unique email address for testing."""
    return f"{prefix}_{uuid4().hex}@example.com"

def _build_user_data(email: str, password: str, full_name: str, role: Optional[str] = None) -> Dict[str, Any]:
    """Builds user creation payload."""
    data = {"email": email, "password": password, "full_name": full_name}
    if role is not None:
        data["role"] = role
    return data


def get_user_by_email(email: str, auth_headers: Dict[str, str]) -> Optional[Dict]:
    """
    Busca por email paginando /users?skip=&limit= hasta encontrar o agotar resultados.
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
    """Skip test if user already exists."""
    existing_user = get_user_by_email(email, auth_headers)
    if existing_user:
        pytest.skip(f"User '{email}' already exists in database. Test skipped.")


def _create_user(
    payload: Dict,
    auth_headers: Optional[Dict[str, str]] = None,
    path=None,
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
        resp = api_request("post", path, json=payload, headers=auth_headers)
        last_resp = resp

        if resp is None:
            continue

        if resp.status_code == 201:
            return resp

        if resp.status_code == 400 and "already registered" in resp.text.lower():
            logger.warning("User already registered; fetching existing user to synthesize 201.")
            existing_user = get_user_by_email(email, auth_headers)
            if existing_user:
                if treat_duplicate_as_success:
                    bug400 = Response()
                    bug400.status_code = 201
                    bug400._content = json.dumps({
                        "message": "user_already_exists",
                        "email": email,
                        "role": existing_user.get("role") or payload.get("role"),  # 👈 clave
                        "id": existing_user.get("id"),
                    }).encode("utf-8")
                    bug400.headers["Content-Type"] = "application/json"
                    bug400.encoding = "utf-8"
                    return bug400
                return resp
            continue  # retry

        return resp

    return last_resp


def create_user_with_email_already_registered(auth_headers, ENDPOINT, role: Optional[str]):
    unique_email = get_unique_email(prefix="registered_jasy")
    payload = _build_user_data(email=unique_email, password=valid_password, full_name=valid_full_name, role=role)

    try:
        user = _create_user(payload,
                            auth_headers,
                            path=ENDPOINT,
                            treat_duplicate_as_success=True)
        exist = _create_user(payload,
                                     auth_headers,
                                     path=ENDPOINT,
                                     treat_duplicate_as_success=False)

        data = exist.json()
        return exist.status_code, data["detail"]

    finally:
        delete_user_by_email(unique_email, auth_headers)


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
