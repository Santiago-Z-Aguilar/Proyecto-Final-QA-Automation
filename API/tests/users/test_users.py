# tests/users/test_users

from API.utils.user_helpers import create_user_with_email_already_registered
from API.utils.settings import USERS, USERS_ME
from API.utils.data import *
from API.utils.api_helpers import api_request

# ---------- POST ----------
class TestPostUsers:
    def test_user_with_email_already_registered(self, auth_headers):
        status_code, detail = create_user_with_email_already_registered(auth_headers, USERS, role='admin')
        assert status_code == 400

    def test_create_admin_user_as_admin(self, auth_headers, create_user_as_admin):
        role = admin_role
        status_code, detail = create_user_as_admin(role=role)
        assert status_code == 201
        assert role in detail['role'], f'Expected role {role}, but got {detail['role']}'

    def test_create_passenger_user_as_admin(self, auth_headers, create_user_as_admin):
        role = passenger_role
        status_code, detail = create_user_as_admin(role=role)
        assert status_code == 201
        assert role in detail['role'], f'Expected role {role}, but got {detail['role']}'

    def test_create_user_with_invalid_role_value(self, auth_headers, create_user_as_admin):
        role = invalid_role
        status_code, detail = create_user_as_admin(role=role)
        assert status_code == 422
        expected_roles_response = detail["detail"][0]["ctx"]["expected"]
        assert passenger_role and admin_role in expected_roles_response

    def test_create_user_with_invalid_email_format(self, auth_headers, create_user_as_admin):

        expected_status = 422
        status_code, detail = create_user_as_admin(email=invalid_email)

        assert status_code == expected_status, (
            f"Se esperaba {expected_status} pero se obtuvo {status_code} "
            f"para email '{invalid_email}', respuesta={detail}"
        )
        assert "address must have an @-sign." in detail["detail"][0]["msg"]

    def test_create_user_with_missing_email(self, auth_headers, create_user_as_admin):
        expected_status = 422
        status_code, detail = create_user_as_admin(email=None)

        assert status_code == expected_status, (
            f"Se esperaba {expected_status} pero se obtuvo {status_code} "
            f"para email None, respuesta={detail}"
        )

    def test_create_user_with_missing_password(self, auth_headers, create_user_as_admin):
        expected_status = 422

        status_code, detail = create_user_as_admin(password=None)

        assert status_code == expected_status, (
            f"Se esperaba {expected_status} pero se obtuvo {status_code} "
            f"para password None, respuesta={detail}"
        )

    def test_create_user_with_missing_full_name(self, auth_headers, create_user_as_admin):
        expected_status = 422

        status_code, detail = create_user_as_admin(full_name=None)

        assert status_code == expected_status, (
            f"Se esperaba {expected_status} pero se obtuvo {status_code} "
            f"para full name None, respuesta={detail}"
        )

    def test_create_user_without_authentication(self, create_user_without_authentication):
        expected_status = 401

        status_code, detail = create_user_without_authentication

        assert  status_code == expected_status, (
            f"Se esperaba {expected_status} pero se obtuvo {status_code} "
            f"para create user without autentication, respuesta={detail}"
        )

    def test_create_admin_user_as_passenger(self, auth_headers, passenger_headers, create_user_as_passenger):
        role = admin_role
        expected_status_code = 403
        status_code, detail = create_user_as_passenger(role=role)
        assert status_code == expected_status_code
        assert "Admin privileges required" in detail["detail"],(
            f"Se esperaba {expected_status_code} pero se obtuvo {status_code} "
            f"para create admin user as passenger, respuesta={detail}"
        )

    def test_create_passenger_user_as_passenger(aself, auth_headers, passenger_headers, create_user_as_passenger):
        role = passenger_role
        status_code, detail = create_user_as_passenger(role=role)
        assert status_code == 403
        assert "Admin privileges required" in detail["detail"]


# ---------- GET ----------
DEFAULT_PAGE_SIZE = 10




def test_list_users_default_pagination(auth_headers, seed_15_passengers):
    resp = api_request("get", USERS, headers=auth_headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) <= DEFAULT_PAGE_SIZE


def test_list_users_skip_limit(auth_headers, seed_15_passengers):
    resp = api_request("get", USERS, headers=auth_headers, params={"skip": 10, "limit": 5})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 5


def test_list_users_invalid_skip_negative(auth_headers):
    resp = api_request("get", USERS, headers=auth_headers, params={"skip": -1})
    assert resp is not None
    assert resp.status_code in (400, 422), f"Se esperaba 400/422. Recibido {resp.status_code}"
    try:
        detail = resp.json().get("detail", "")
    except Exception:
        detail = resp.text or ""
    msg = (detail or "").lower()
    assert "skip" in msg and any(s in msg for s in ["must be >= 0", "no puede ser negativo", ">= 0"]), \
        f"Mensaje de validación poco claro: {detail}"


def test_list_users_without_token():
    resp = api_request("get", USERS)
    assert resp.status_code == 401, f"Se esperaba 401. Recibido {resp.status_code}"
    body = resp.json()
    assert body.get("detail") == "Not authenticated"


def test_list_users_with_passenger_token(passenger_headers):
    resp = api_request("get", USERS, headers=passenger_headers)
    assert resp.status_code == 403, f"Se esperaba 403. Recibido {resp.status_code}"
    body = resp.json()
    assert body.get("detail") in ("Admin privileges required", "Forbidden")


def test_me_with_valid_token(auth_headers):
    resp = api_request("get", USERS_ME, headers=auth_headers)
    assert resp.status_code == 200, resp.text
    me = resp.json()
    for key in ("id", "email", "full_name", "role"):
        assert key in me, f"Falta campo '{key}' en /users/me"


def test_me_without_token():
    resp = api_request("get", USERS_ME)
    assert resp.status_code == 401, f"Se esperaba 401. Recibido {resp.status_code}"
    body = resp.json()
    assert body.get("detail") == "Not authenticated"


def test_skip_beyond_total_returns_empty(auth_headers, seed_15_passengers):
    resp = api_request("get", USERS, headers=auth_headers, params={"skip": 9999, "limit": 10})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert isinstance(data, list)
    assert data == [], f"Con skip grande se esperaba []. Recibido: {data}"


def test_get_existing_users(auth_headers):
    resp = api_request("get", f"{USERS}?limit=100&skip=1", headers=auth_headers)
    print(resp.json())

