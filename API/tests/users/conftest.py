# tests/users/conftest.py
import logging
from uuid import uuid4
import pytest

from API.utils.api_helpers import api_request
from API.utils.settings import USERS, USERS_ME
from API.utils.data import admin_role, passenger_role, valid_password, valid_full_name
from API.utils.user_helpers import (
    _create_user,
    delete_user_by_id,
    _build_user_data,
    get_unique_email,
)

logger = logging.getLogger("Endpoint_USERS")


# ------------------------------ POST helpers ------------------------------
@pytest.fixture
def create_user_as_admin(auth_headers):
    """
    Create users as admin. Yields a callable that returns (status, body).
    Tracks created user IDs and deletes them after the test.
    """
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
    """
    Create users as passenger. Yields a callable that returns (status, body).
    Tracks created user IDs and deletes them after the test (using admin headers).
    """
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

    for uid in created_ids:
        try:
            delete_user_by_id(uid, auth_headers)
        except Exception as e:
            logger.warning(f"Cleanup exception delete_by_id({uid}): {e}")


@pytest.fixture
def create_user_without_authentication():
    """
    Attempt to create a user without headers.
    Returns a callable that yields (status_code, body).
    Typically used to assert 401/403/422 responses.
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
        resp = api_request("post", USERS, json=payload)  # no headers
        body = resp.json() if getattr(resp, "content", None) else {}
        return resp.status_code, body

    return _create


# ------------------------------ GET helpers ------------------------------
@pytest.fixture
def users_get():
    """Return a callable to GET /users with optional headers and params."""
    def _call(headers=None, params=None):
        return api_request("get", USERS, headers=headers, params=params)
    return _call


@pytest.fixture
def me_get():
    """Return a callable to GET /users/me with optional headers."""
    def _call(headers=None):
        return api_request("get", USERS_ME, headers=headers)
    return _call


# ------------------------------ PUT / DELETE helpers ------------------------------
@pytest.fixture
def update(auth_headers):
    """Return a callable to PUT /users/{id} with a payload and explicit headers."""
    def _do(uid, payload, headers):
        return api_request("put", f"{USERS}{uid}", json=payload, headers=headers)
    return _do


@pytest.fixture
def fake_user_id():
    """Return a synthetically generated user-like ID for negative tests."""
    return f"usr_fake-{uuid4().hex[:8]}"


# ------------------------------ Seeds for pagination tests ------------------------------
@pytest.fixture
def seed_15_passengers(create_user_as_admin):
    """
    Create 15 passenger users for pagination tests.
    Cleanup is handled by create_user_as_admin (IDs are tracked and deleted).
    """
    created = []
    for _ in range(15):
        sc, body = create_user_as_admin(role=passenger_role)
        if sc in (200, 201):
            created.append(body["id"])
    yield created
