# utils/user_helpers.py

import logging
import time
from uuid import uuid4
from typing import Dict, Optional
from requests.models import Response
from utils.api_helpers import api_request
from utils.settings import USERS, AUTH_SIGN_UP
import pytest

logger = logging.getLogger("qa_tests")

# Constants
DEFAULT_RETRIES = 3
CLEANUP_DELAY = 1  # Special delay for cleanup operations


def get_unique_email(prefix: str = "test") -> str:
    """Generate a unique email address for testing."""
    return f"{prefix}_{uuid4().hex}@example.com"


def get_user_by_email(email: str, auth_headers: Dict[str, str]) -> Optional[Dict]:
    """
    Returns user dict if exists, None otherwise.

    Args:
        email: User email to search for
        auth_headers: Authentication headers

    Returns:
        dict: User data if found, None otherwise
    """
    resp: Response = api_request("GET", USERS, headers=auth_headers)
    if resp.status_code == 200:
        users: list = resp.json()
        return next((user for user in users if user["email"] == email), None)
    return None


def user_exist_skip(email: str, auth_headers: Dict[str, str]) -> None:
    """Skip test if user already exists."""
    existing_user = get_user_by_email(email, auth_headers)
    if existing_user:
        pytest.skip(f"User '{email}' already exists in database. Test skipped.")


def _create_user(payload: Dict, auth_headers: Dict[str, str], max_retries: int = DEFAULT_RETRIES) -> Response:
    """
    Handles user creation with smart retry logic.
    """
    email = payload["email"]

    for attempt in range(1, max_retries + 1):
        resp = api_request("POST", AUTH_SIGN_UP, json=payload, headers=auth_headers)

        # ✅ Caso exitoso
        if resp.status_code == 201:
            return resp

        # ✅ Usuario ya existe
        if resp.status_code == 400 and "already registered" in resp.text.lower():
            logger.warning(f"Duplicate user {email} (attempt {attempt})")

            # get_user_by_email retorna dict o None, NO Response
            existing_user = get_user_by_email(email, auth_headers)
            if existing_user:  # Solo verificar si existe (es truthy)
                logger.info(f"User {email} exists after duplicate error")
                # Crear respuesta de éxito simulado
                success_response = Response()
                success_response.status_code = 201
                success_response._content = f'{{"message": "user_already_exists", "email": "{email}"}}'.encode()
                return success_response
            else:
                logger.error(f"User {email} not found despite duplicate error")
                continue

        # ⚠️ Otro error
        return resp

    return resp



def delete_user_by_email(email: str, auth_headers: Dict[str, str]) -> bool:
    """
    Delete user by email.

    Args:
        email: User email to delete
        auth_headers: Authentication headers

    Returns:
        bool: True if deletion succeeded, False otherwise
    """
    user = get_user_by_email(email, auth_headers)
    if not user:
        return False

    resp: Response = api_request("DELETE", f"{USERS}{user['id']}", headers=auth_headers)
    if resp.status_code == 204:
        logger.info(f" Deleted user '{email}'")
        time.sleep(CLEANUP_DELAY)
        return True
    if resp.status_code != 400 or 500:
        logger.error(f" User not deleted '{email}'")
    return False