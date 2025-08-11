# utils/user_helpers.py

import logging
import time
from uuid import uuid4
from utils.api_helpers import api_request, RETRIES, DELAY
from utils.settings import USERS, AUTH_SIGN_UP
import pytest

logger = logging.getLogger("qa_tests")

def get_unique_email(prefix="test"):
    return f"{prefix}_{uuid4().hex}@example.com"

def get_user_by_email(email, auth_headers, retries=RETRIES, delay=DELAY):
    """
    Devuelve el usuario como dict si existe, o None si no existe.
    """
    for i in range(retries):
        resp = api_request("get", USERS, headers=auth_headers)
        if resp.status_code == 200:
            users = resp.json()
            return next((user for user in users if user["email"] == email), None)
        elif resp.status_code == 500:
            logger.warning(f"/users returned 500, retrying ({i+1}/{retries}) after {delay}s...")
            time.sleep(delay)
        else:
            logger.error(f"/users returned unexpected status: {resp.status_code}")
            break
    return None

# def create_user_signup(email, auth_headers, retries=RETRIES, delay=DELAY):
#     r = api_request("post", AUTH_SIGN_UP)


def user_exist_skip(email, auth_headers):
    """Check if user already exists and skip test if true."""
    existing_user = get_user_by_email(email, auth_headers)
    if existing_user:
        pytest.skip(f"User '{email}' already exists in database. Test skipped.")

def _create_user(payload, auth_headers, max_retries=3):
    """
    Handles signup with retries ONLY for 400 (already exists).
    Returns first 201, first 400, or last error.
    """
    email = payload["email"]
    first_response = None

    for attempt in range(1, max_retries + 1):
        resp = api_request("post", AUTH_SIGN_UP, json=payload)

        # Guarda la primera respuesta para diagnóstico
        if first_response is None:
            first_response = resp

        # Éxito: retorna inmediatamente
        if resp.status_code == 201:
            return resp

        # Usuario duplicado: maneja reintento
        if resp.status_code == 400 and "already registered" in resp.text.lower():
            logger.warning(f"Duplicate user (attempt {attempt}/{max_retries})")
            if attempt < max_retries:
                if not delete_user_by_email(email, auth_headers):
                    logger.error(f"Failed to delete {email}")
                    break
            continue

        # Otros errores (incluyendo 500): continúa el bucle para reintentar
        logger.warning(f"Received {resp.status_code} (attempt {attempt}/{max_retries})")

    # Si llegamos aquí, retorna:
    # - El primer 400 (si existió)
    # - O la última respuesta (500, 422, etc.)
    return first_response if (first_response and first_response.status_code == 400) else resp

def delete_user_by_email(email, auth_headers, retries=RETRIES, delay=DELAY):
    user = get_user_by_email(email, auth_headers, retries, delay)
    if user:
        user_id = user["id"]
        for i in range(retries):
            resp = api_request("delete", f"{USERS}{user_id}", headers=auth_headers)
            if resp.status_code == 204:
                logger.info(f"🧹 Cleanup: Deleted user '{email}' after test.")
                time.sleep(3)
                return True
            elif resp.status_code == 500:
                logger.warning(f"Delete user 500, retrying ({i+1}/{retries}) after {delay}s...")
                time.sleep(delay)
            else:
                logger.error(f"Delete user returned unexpected status: {resp.status_code}")
                break
    return False
