# tests/users/test_users
from enum import verify

from API.tests.conftest import auth_headers
from API.utils.user_helpers import create_user_with_email_already_registered, get_unique_email, delete_user_by_id
from API.utils.settings import USERS
from API.tests.users.data_users import *
from API.utils.api_helpers import api_request

# ---------- POST ----------
class TestPostUsers:
    def test_user_with_email_already_registered(self, auth_headers):
        status_code, detail = create_user_with_email_already_registered(auth_headers, USERS, role='admin')
        assert status_code == 400

    def test_create_admin_user_as_admin(self, auth_headers, create_user_as_admin):
        status_code, detail = create_user_as_admin(role=admin_role)
        assert status_code == 201
        assert admin_role in detail['role'], f'Expected role {admin_role}, but got {detail['role']}'

    def test_create_passenger_user_as_admin(self, auth_headers, create_user_as_admin):
        status_code, detail = create_user_as_admin(role=passenger_role)
        assert status_code == 201
        assert passenger_role in detail['role'], f'Expected role {passenger_role}, but got {detail['role']}'

    def test_create_user_with_invalid_role_value(self, auth_headers, create_user_as_admin):
        status_code, detail = create_user_as_admin(role=invalid_role)
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

        status_code, detail = create_user_as_admin(include_email=False)

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

        status_code, detail = create_user_without_authentication()

        assert  status_code == expected_status, (
            f"Se esperaba {expected_status} pero se obtuvo {status_code} "
            f"para create user without autentication, respuesta={detail}"
        )

    def test_create_admin_user_as_passenger(self, auth_headers, passenger_headers, create_user_as_passenger):
        expected_status_code = 403
        status_code, detail = create_user_as_passenger(role=admin_role)
        assert status_code == expected_status_code
        assert "Admin privileges required" in detail["detail"],(
            f"Se esperaba {expected_status_code} pero se obtuvo {status_code} "
            f"para create admin user as passenger, respuesta={detail}"
        )

    def test_create_passenger_user_as_passenger(self, auth_headers, passenger_headers, create_user_as_passenger):
        status_code, detail = create_user_as_passenger(role=passenger_role)
        assert status_code == 403
        assert "Admin privileges required" in detail["detail"]

# ---------- GET ----------
class TestGetUsers:
    """Suite de pruebas para endpoints GET de /users y /users/me."""

    def test_list_users_default_pagination(self, auth_headers, seed_15_passengers, users_get):
        resp = users_get(headers=auth_headers)
        assert resp is not None
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert isinstance(data, list), f"Se esperaba lista. Body: {resp.text}"
        assert len(data) <= DEFAULT_PAGE_SIZE, f"Max {DEFAULT_PAGE_SIZE}, recibido {len(data)}"

    def test_list_users_skip_limit(self, auth_headers, seed_15_passengers, users_get):
        resp = users_get(headers=auth_headers, params={"skip": 5, "limit": 5})
        assert resp is not None
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert isinstance(data, list), f"Se esperaba lista. Body: {resp.text}"
        assert len(data) == 5, f"Largo esperado 5, recibido {len(data)}"

    def test_list_users_invalid_skip_negative(self, auth_headers, users_get):
        resp = users_get(headers=auth_headers, params={"skip": -1})
        assert resp is not None
        assert resp.status_code in (400, 422), f"Se esperaba 400/422. Recibido {resp.status_code}. Body: {resp.text}"

    def test_list_users_without_token(self, users_get):
        resp = users_get()  # sin headers
        assert resp is not None
        assert resp.status_code == 401, f"Se esperaba 401. Recibido {resp.status_code}. Body: {resp.text}"
        body = resp.json()
        assert body.get("detail") == "Not authenticated", f"Detalle inesperado: {body}"

    def test_list_users_with_passenger_token(self, passenger_headers, users_get):
        resp = users_get(headers=passenger_headers)
        assert resp is not None
        assert resp.status_code == 403, f"Se esperaba 403. Recibido {resp.status_code}. Body: {resp.text}"
        body = resp.json()
        assert body.get("detail") in ("Admin privileges required", "Forbidden"), f"Detalle inesperado: {body}"

    def test_me_with_valid_token(self, auth_headers, me_get):
        resp = me_get(headers=auth_headers)
        assert resp is not None
        assert resp.status_code == 200, resp.text
        me = resp.json()
        assert isinstance(me, dict), f"Se esperaba dict. Body: {resp.text}"
        for key in ("id", "email", "full_name", "role"):
            assert key in me, f"Falta campo '{key}' en /users/me: {me}"

    def test_me_without_token(self, me_get):
        resp = me_get()  # sin headers
        assert resp is not None
        assert resp.status_code == 401, f"Se esperaba 401. Recibido {resp.status_code}. Body: {resp.text}"
        body = resp.json()
        assert body.get("detail") == "Not authenticated", f"Detalle inesperado: {body}"

    def test_skip_beyond_total_returns_empty(self, auth_headers, seed_15_passengers, users_get):
        resp = users_get(headers=auth_headers, params={"skip": 9999, "limit": 10})
        assert resp is not None
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert isinstance(data, list), f"Se esperaba lista. Body: {resp.text}"
        assert data == [], f"Con skip grande se esperaba []. Recibido: {data}"

# ---------- PUT ----------
class TestPutUsers:

    def test_update_user_with_valid_data_as_admin(self, create_user_as_admin, do_update, auth_headers):
        email = get_unique_email(prefix="user_to_upd")
        sc, detail = create_user_as_admin(email=email, role=passenger_role )
        uid = detail["id"]

        resp = do_update(uid, valid_update_payload, auth_headers)
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["id"] == uid
        assert body["email"] == valid_update_payload["email"]
        assert body["full_name"] == valid_update_payload["full_name"]
        assert "password" not in body
        assert body["role"] == passenger_role

    def test_update_user_with_invalid_email(self, create_user_as_admin, do_update, auth_headers):
        sc, detail = create_user_as_admin(role=passenger_role)
        uid = detail["id"]

        resp = do_update(uid, invalid_email_payload, auth_headers)
        assert resp.status_code == 422, f"Esperado 422, recibido {resp.status_code}: {resp.text}"
        det = resp.json().get("detail", [])
        assert isinstance(det, list) and det
        assert ("@-sign" in det[0].get("msg", "")) or ("valid email" in det[0].get("msg", ""))

    def test_update_non_existent_user_id(self, fake_user_id, do_update, auth_headers):
        resp = do_update(fake_user_id, valid_update_payload, auth_headers)
        assert resp.status_code == 404, f"Esperado 404, recibido {resp.status_code}: {resp.text}"
        assert resp.json().get("detail", "").lower() in ("not found", "no encontrado")

    def test_update_user_role_as_admin(self, create_user_as_admin, do_update, auth_headers):
        sc, detail = create_user_as_admin(role=passenger_role)
        uid = detail["id"]

        resp = do_update(uid, update_role_payload, auth_headers)
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["email"] == update_role_payload["email"]
        assert body["full_name"] == update_role_payload["full_name"]
        assert body["role"] == passenger_role
        print(body)

    def test_update_user_as_passenger_forbidden(self, create_user_as_admin, do_update, passenger_headers):
        sc, detail = create_user_as_admin(role=passenger_role)
        uid = detail["id"]

        resp = do_update(uid, valid_update_payload, headers=passenger_headers)
        assert resp.status_code == 403, f"Esperado 403, recibido {resp.status_code}: {resp.text}"
        assert resp.json().get("detail") in ("Forbidden", "Admin privileges required")

# ---------- Delete ----------
class TestDeleteUsers:

    def test_delete_existing_user_as_admin(self, create_user_as_admin, users_get, auth_headers):
        sc, detail = create_user_as_admin(role=passenger_role)
        uid = detail["id"]

        delete = delete_user_by_id(uid, auth_headers)
        assert delete is True

        resp = users_get(auth_headers, params={"skip": 0, "limit": 100})
        assert resp.status_code == 200, resp.text
        users = resp.json()

        ids = [u["id"] for u in users]
        assert uid not in ids, f"Usuario {uid} no eliminado correctamente"

    def test_delete_non_existent_user_id_as_admin(self, fake_user_id, auth_headers):
        resp = api_request("delete", f"{USERS}{fake_user_id}", headers=auth_headers)
        assert resp.status_code == 404, f"Esperado 404, recibido {resp.status_code}: {resp.text}"

    def test_delete_user_without_token(self, create_user_as_admin):
        sc, detail = create_user_as_admin(role=passenger_role)
        uid = detail["id"]


        resp = api_request("delete", f"{USERS}{uid}")
        assert resp.status_code == 401, f"Esperado 401, recibido {resp.status_code}: {resp.text}"
        assert resp.json().get("detail") == "Not authenticated"

    def test_delete_user_with_passenger_token(self, create_user_as_admin, passenger_headers):
        sc, detail = create_user_as_admin(role=passenger_role)
        assert sc in (200, 201)
        uid = detail["id"]

        resp = api_request("delete", f"{USERS}{uid}", headers=passenger_headers)
        assert resp.status_code == 403, f"Esperado 403, recibido {resp.status_code}: {resp.text}"
        assert resp.json().get("detail") in ("Admin privileges required", "Forbidden")
