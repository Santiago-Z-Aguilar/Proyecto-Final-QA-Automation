# tests/users/conftest.py
import logging
from uuid import uuid4
import pytest

from API.utils.api_helpers import api_request
from API.utils.settings import USERS, USERS_ME
from API.utils.data import admin_role, passenger_role, valid_password, valid_full_name
from API.utils.user_helpers import (
    _create_user,
    get_user_by_email,  # fallback por seguridad
    delete_user_by_id,
    _build_user_data, get_unique_email,
)

logger = logging.getLogger("Endpoint_USERS")


# ======================================================================
# POST helpers
# ======================================================================
@pytest.fixture
def create_user_as_admin(auth_headers):
    created_ids = []

    def _create(
        *,
        email: str | None = None,
        password: str | None = valid_password,
        full_name: str | None = valid_full_name,
        role: str = admin_role,
        include_email: bool = True,
    ):
        if email is None and include_email:
            email = get_unique_email(prefix="admin_user")

        payload = _build_user_data(
            email=email if include_email else None,
            password=password,
            full_name=full_name,
            role=role,
        )

        resp = _create_user(payload, auth_headers, path=USERS)
        status = resp.status_code
        body = resp.json() if getattr(resp, "content", None) else {}

        if status in (200, 201) and "id" in body:
            created_ids.append(body["id"])

        return status, body

    yield _create

    for uid in created_ids:
        try:
            delete_user_by_id(uid, auth_headers)
        except Exception as e:
            logger.warning(f"Cleanup exception delete_by_id({uid}): {e}")

@pytest.fixture
def create_user_as_passenger(passenger_headers, auth_headers):
    created_ids = []

    def _create(
        *,
        email: str | None = None,
        password: str = valid_password,
        full_name: str = valid_full_name,
        role: str = passenger_role,
    ):
        payload = _build_user_data(
            email=email,
            password=password,
            full_name=full_name,
            role=role,
        )
        resp = _create_user(payload, passenger_headers, path=USERS)
        status = resp.status_code
        body = resp.json() if getattr(resp, "content", None) else {}

        if status in (200, 201) and "id" in body:
            created_ids.append(body["id"])

        return status, body

    yield _create

    # Limpieza al terminar
    for uid in created_ids:
        try:
            delete_user_by_id(uid, auth_headers)
        except Exception as e:
            logger.warning(f"Cleanup exception delete_by_id({uid}): {e}")

@pytest.fixture
def create_user_without_authentication():
    """
    Intenta crear usuario SIN headers y devuelve (status_code, body).
    """
    def _create(
        *,
        email: str | None = None,
        password: str = valid_password,
        full_name: str = valid_full_name,
        role: str = passenger_role,
    ):
        payload = _build_user_data(
            email=email,
            password=password,
            full_name=full_name,
            role=role,
        )
        resp = api_request("post", USERS, json=payload)  # sin headers
        body = resp.json() if getattr(resp, "content", None) else {}
        return resp.status_code, body

    return _create



# ======================================================================
# GET callers
# ======================================================================
@pytest.fixture
def users_get():
    def _call(headers=None, params=None):
        return api_request("get", USERS, headers=headers, params=params)
    return _call


@pytest.fixture
def me_get():
    def _call(headers=None):
        return api_request("get", USERS_ME, headers=headers)
    return _call


# ======================================================================
# PUT / DELETE helpers
# ======================================================================
@pytest.fixture
def do_update(auth_headers):
    def _do(uid, payload, headers):
        return api_request("put", f"{USERS}{uid}", json=payload, headers=headers)
    return _do


# @pytest.fixture
# def do_delete_id(auth_headers):
#     def _delete(uid, headers=None):
#         if headers and headers is not auth_headers:
#             return api_request("delete", f"{USERS}/{uid}", headers=headers)
#         return delete_user_by_id(uid, auth_headers)
#     return _delete


@pytest.fixture
def fake_user_id():
    return f"usr_fake-{uuid4().hex[:8]}"


# ======================================================================
# Seeds para pruebas de GET (paginación)
# ======================================================================
@pytest.fixture
def seed_15_passengers(create_user_as_admin):
    """
    Crea N pasajeros para probar paginación.
    La limpieza la hace create_user_as_admin automáticamente.
    """
    created = []
    for _ in range(15):
        sc, body = create_user_as_admin(role=passenger_role)
        if sc in (200, 201):
            created.append(body["id"])
    yield created
