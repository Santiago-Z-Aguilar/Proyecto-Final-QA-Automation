# tests/users/conftest.py
from API.utils.api_helpers import api_request
from API.utils.data import valid_password, valid_full_name, admin_role, passenger_role
from API.utils.user_helpers import _create_user, _build_user_data, delete_user_by_email, get_unique_email, \
    get_user_by_email
from API.utils.settings import USERS
from typing import List, Dict
import pytest
import logging

logger = logging.getLogger("Endpoint_USERS")

@pytest.fixture
def create_user_as_admin(auth_headers):
    """Fixture to create users as administrator with automatic cleanup."""
    created_users = []

    def _create_user_fixture(
            email: str = None,
            role: str = admin_role,
            password: str = valid_password,
            full_name: str = valid_full_name,
            **kwargs  # Additional arguments for _create_user
    ):
        # Generate unique email if not provided
        user_email = email or get_unique_email(prefix="admin_user_jasy")

        # Build and send payload
        payload = _build_user_data(user_email, password, full_name, role)
        response = _create_user(payload, auth_headers, path=USERS, **kwargs)

        # Register user for cleanup only if creation was successful (201) or duplicate treated as success
        if response.status_code in [200, 201]:
            created_users.append(user_email)

        return response.status_code, response.json()

    yield _create_user_fixture

    # Cleanup: delete all successfully created users
    for email in created_users:
        try:
            delete_user_by_email(email, auth_headers)
            logging.info(f"User {email} successfully deleted")
        except Exception as e:
            logging.warning(f"Failed to delete user {email}: {e}")


@pytest.fixture
def create_user_as_passenger(auth_headers, passenger_headers):
    """Fixture to create users as passenger with automatic cleanup."""
    created_users = []

    def _create_user_fixture(
            email: str = None,
            role: str = passenger_role,
            password: str = valid_password,
            full_name: str = valid_full_name,
            **kwargs  # Additional arguments for _create_user
    ):
        # Generate unique email if not provided
        user_email = email or get_unique_email(prefix="passenger_user_jasy")

        # Build and send payload
        payload = _build_user_data(user_email, password, full_name, role)
        response = _create_user(payload, passenger_headers, path=USERS, **kwargs)

        # Register user for cleanup only if creation was successful (201) or duplicate treated as success
        if response.status_code in [200, 201]:
            created_users.append(user_email)

        return response.status_code, response.json()

    yield _create_user_fixture

    # Cleanup: delete all successfully created users using admin privileges
    for email in created_users:
        try:
            delete_user_by_email(email, auth_headers)
            logging.info(f"User {email} successfully deleted")
        except Exception as e:
            logging.warning(f"Failed to delete user {email}: {e}")


@pytest.fixture()
def create_user_without_authentication():
    """Fixture to create users without_authentication. No cleanup needed."""
    # Generate unique email if not provided
    user_email = get_unique_email(prefix="without_authentication_jasy")

    # Build and send payload
    payload = _build_user_data(user_email, password=valid_password, full_name=valid_full_name, role=None)

    resp = _create_user(payload, path=USERS)
    return resp.status_code, resp.json()


# ---------- Helpers de tests de get ----------
@pytest.fixture(scope="session")
def seed_15_passengers(auth_headers):
    created = []  # (email, id)
    try:
        for _ in range(15):
            email = get_unique_email(prefix="bulk_passenger")
            payload = _build_user_data(email, valid_password, valid_full_name, passenger_role)
            resp = _create_user(payload, auth_headers, path=USERS, treat_duplicate_as_success=True)

            if resp is None:
                raise RuntimeError("api_request devolvió None al crear usuario")

            if resp.status_code in (200, 201):
                data = resp.json()
            elif resp.status_code == 400 and "already registered" in resp.text.lower():
                # Con el fix de get_user_by_email paginado, _create_user normalmente devolverá 201 sintético.
                # Si aún llega 400 aquí, forzamos la búsqueda y continuamos.
                user = get_user_by_email(email, auth_headers)
                if not user:
                    raise AssertionError(f"Duplicado reportado pero no encontrado en listado para {email}")
                data = {"id": user["id"], "email": email}
            else:
                raise AssertionError(f"Error creando usuario: {resp.status_code} {getattr(resp, 'text','')}")

            uid = data.get("id")
            if not uid:
                # Fallback extra por si la respuesta no trae id
                user = get_user_by_email(email, auth_headers)
                if not user or not user.get("id"):
                    raise AssertionError(f"No se pudo obtener id para {email}")
                uid = user["id"]

            created.append((email, uid))

        # Si llegamos aquí, ya hay 15 creados
        yield [email for (email, _) in created]

    finally:
        # Cleanup SIEMPRE corre, aunque falle arriba
        for email, uid in created:
            resp = api_request("DELETE", f"{USERS.rstrip('/')}/{uid}", headers=auth_headers)
            ok = bool(resp and resp.status_code in (200, 202, 204))
            logger.info(f"Cleanup {'✅' if ok else '❌'} {email} ({uid}) -> {resp and resp.status_code}")


