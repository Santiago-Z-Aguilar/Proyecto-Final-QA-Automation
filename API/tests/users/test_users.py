# tests/auth/test_auth.py
from API.utils.user_helpers import (
    create_user_with_email_already_registered,
    get_unique_email,
    delete_user_by_id,
)
from API.utils.settings import USERS
from API.tests.users.data_users import *
from API.utils.api_helpers import api_request


# ---------- POST ----------
class TestPostUsers:

    def test_user_with_email_already_registered(self, auth_headers):
        status_code, detail = create_user_with_email_already_registered(auth_headers, USERS, role="admin")
        assert status_code == 400, f"Expected 400, got {status_code}. Response: {detail}"

    def test_create_admin_user_as_admin(self, auth_headers, create_user_as_admin):
        status_code, detail = create_user_as_admin(role=admin_role)
        assert status_code == 201, f"Expected 201, got {status_code}. Response: {detail}"
        assert admin_role in detail["role"], f"Expected role '{admin_role}', got '{detail['role']}'"

    def test_create_passenger_user_as_admin(self, auth_headers, create_user_as_admin):
        status_code, detail = create_user_as_admin(role=passenger_role)
        assert status_code == 201, f"Expected 201, got {status_code}. Response: {detail}"
        assert passenger_role in detail["role"], f"Expected role '{passenger_role}', got '{detail['role']}'"

    def test_create_user_with_invalid_role_value(self, auth_headers, create_user_as_admin):
        status_code, detail = create_user_as_admin(role=invalid_role)
        assert status_code == 422, f"Expected 422, got {status_code}. Response: {detail}"
        expected_roles_response = detail["detail"][0]["ctx"]["expected"]
        assert passenger_role in expected_roles_response or admin_role in expected_roles_response, (
            f"Expected roles {admin_role} or {passenger_role}, got {expected_roles_response}"
        )

    def test_create_user_with_invalid_email_format(self, auth_headers, create_user_as_admin):
        expected_status = 422
        status_code, detail = create_user_as_admin(email=invalid_email)
        assert status_code == expected_status, (
            f"Expected {expected_status}, got {status_code} for email '{invalid_email}'. Response: {detail}"
        )
        assert "address must have an @-sign." in detail["detail"][0]["msg"]

    def test_create_user_with_missing_email(self, auth_headers, create_user_as_admin):
        expected_status = 422
        status_code, detail = create_user_as_admin(include_email=False)
        assert status_code == expected_status, (
            f"Expected {expected_status}, got {status_code} for missing email. Response: {detail}"
        )

    def test_create_user_with_missing_password(self, auth_headers, create_user_as_admin):
        expected_status = 422
        status_code, detail = create_user_as_admin(password=None)
        assert status_code == expected_status, (
            f"Expected {expected_status}, got {status_code} for missing password. Response: {detail}"
        )

    def test_create_user_with_missing_full_name(self, auth_headers, create_user_as_admin):
        expected_status = 422
        status_code, detail = create_user_as_admin(full_name=None)
        assert status_code == expected_status, (
            f"Expected {expected_status}, got {status_code} for missing full name. Response: {detail}"
        )

    def test_create_user_without_authentication(self, create_user_without_authentication):
        expected_status = 401
        status_code, detail = create_user_without_authentication()
        assert status_code == expected_status, (
            f"Expected {expected_status}, got {status_code} when creating user without authentication. Response: {detail}"
        )

    def test_create_admin_user_as_passenger(self, create_user_as_passenger):
        expected_status_code = 403
        status_code, detail = create_user_as_passenger(role=admin_role)
        assert status_code == expected_status_code, (
            f"Expected {expected_status_code}, got {status_code} when creating admin user as passenger. Response: {detail}"
        )
        assert "Admin privileges required" in detail["detail"]

    def test_create_passenger_user_as_passenger(self, create_user_as_passenger):
        status_code, detail = create_user_as_passenger(role=passenger_role)
        assert status_code == 403, f"Expected 403, got {status_code}. Response: {detail}"
        assert "Admin privileges required" in detail["detail"]


# ---------- GET ----------
class TestGetUsers:

    def test_list_users_default_pagination(self, auth_headers, seed_15_passengers, users_get):
        resp = users_get(headers=auth_headers)
        assert resp is not None
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}. Body: {resp.text}"
        data = resp.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}. Body: {resp.text}"
        assert len(data) <= DEFAULT_PAGE_SIZE, f"Expected <= {DEFAULT_PAGE_SIZE}, got {len(data)}"

    def test_list_users_skip_limit(self, auth_headers, seed_15_passengers, users_get):
        resp = users_get(headers=auth_headers, params={"skip": 5, "limit": 5})
        assert resp is not None
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}. Body: {resp.text}"
        data = resp.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}. Body: {resp.text}"
        assert len(data) == 5, f"Expected 5, got {len(data)}"

    def test_list_users_invalid_skip_negative(self, auth_headers, users_get):
        resp = users_get(headers=auth_headers, params={"skip": -1})
        assert resp is not None
        assert resp.status_code in (400, 422), f"Expected 400/422, got {resp.status_code}. Body: {resp.text}"

    def test_list_users_without_token(self, users_get):
        resp = users_get()
        assert resp is not None
        assert resp.status_code == 401, f"Expected 401, got {resp.status_code}. Body: {resp.text}"
        body = resp.json()
        assert body.get("detail") == "Not authenticated", f"Unexpected detail: {body}"

    def test_list_users_with_passenger_token(self, passenger_headers, users_get):
        resp = users_get(headers=passenger_headers)
        assert resp is not None
        assert resp.status_code == 403, f"Expected 403, got {resp.status_code}. Body: {resp.text}"
        body = resp.json()
        assert body.get("detail") in ("Admin privileges required", "Forbidden"), f"Unexpected detail: {body}"

    def test_me_with_valid_token(self, auth_headers, me_get):
        resp = me_get(headers=auth_headers)
        assert resp is not None
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}. Body: {resp.text}"
        me = resp.json()
        assert isinstance(me, dict), f"Expected dict, got {type(me)}. Body: {resp.text}"
        for key in ("id", "email", "full_name", "role"):
            assert key in me, f"Missing key '{key}' in /users/me response: {me}"

    def test_me_without_token(self, me_get):
        resp = me_get()
        assert resp is not None
        assert resp.status_code == 401, f"Expected 401, got {resp.status_code}. Body: {resp.text}"
        body = resp.json()
        assert body.get("detail") == "Not authenticated", f"Unexpected detail: {body}"

    def test_skip_beyond_total_returns_empty(self, auth_headers, seed_15_passengers, users_get):
        resp = users_get(headers=auth_headers, params={"skip": 9999, "limit": 10})
        assert resp is not None
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}. Body: {resp.text}"
        data = resp.json()
        assert isinstance(data, list), f"Expected list, got {type(data)}. Body: {resp.text}"
        assert data == [], f"Expected [], got {data}"


# ---------- PUT ----------
class TestPutUsers:

    def test_update_user_with_valid_data_as_admin(self, create_user_as_admin, update, auth_headers):
        email = get_unique_email(prefix="user_to_upd")
        sc, detail = create_user_as_admin(email=email, role=passenger_role)
        uid = detail["id"]

        resp = update(uid, valid_update_payload, auth_headers)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}. Body: {resp.text}"
        body = resp.json()
        assert body["id"] == uid, f"Expected id {uid}, got {body['id']}"
        assert body["email"] == valid_update_payload["email"], f"Expected email {valid_update_payload['email']}, got {body['email']}"
        assert body["full_name"] == valid_update_payload["full_name"], f"Expected full_name {valid_update_payload['full_name']}, got {body['full_name']}"
        assert "password" not in body, f"Password should not be in response. Body: {body}"
        assert body["role"] == passenger_role, f"Expected role {passenger_role}, got {body['role']}"

    def test_update_user_with_invalid_email(self, create_user_as_admin, update, auth_headers):
        sc, detail = create_user_as_admin(role=passenger_role)
        uid = detail["id"]

        resp = update(uid, invalid_email_payload, auth_headers)
        assert resp.status_code == 422, f"Expected 422, got {resp.status_code}. Body: {resp.text}"
        det = resp.json().get("detail", [])
        assert isinstance(det, list) and det, f"Expected list detail, got {det}"
        assert ("@-sign" in det[0].get("msg", "")) or ("valid email" in det[0].get("msg", "")), f"Unexpected msg: {det}"

    def test_update_non_existent_user_id(self, fake_user_id, update, auth_headers):
        resp = update(fake_user_id, valid_update_payload, auth_headers)
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}. Body: {resp.text}"
        assert resp.json().get("detail", "").lower() in ("not found", "no encontrado")

    def test_update_user_role_as_admin(self, create_user_as_admin, update, auth_headers):
        sc, detail = create_user_as_admin(role=passenger_role)
        uid = detail["id"]

        resp = update(uid, update_role_payload, auth_headers)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}. Body: {resp.text}"
        body = resp.json()
        assert body["email"] == update_role_payload["email"], f"Expected email {update_role_payload['email']}, got {body['email']}"
        assert body["full_name"] == update_role_payload["full_name"], f"Expected full_name {update_role_payload['full_name']}, got {body['full_name']}"
        assert body["role"] == passenger_role, f"Expected role {passenger_role}, got {body['role']}"

    def test_update_user_as_passenger_forbidden(self, create_user_as_admin, update, passenger_headers):
        sc, detail = create_user_as_admin(role=passenger_role)
        uid = detail["id"]

        resp = update(uid, valid_update_payload, headers=passenger_headers)
        assert resp.status_code == 403, f"Expected 403, got {resp.status_code}. Body: {resp.text}"
        assert resp.json().get("detail") in ("Forbidden", "Admin privileges required")


# ---------- DELETE ----------
class TestDeleteUsers:

    def test_delete_existing_user_as_admin(self, create_user_as_admin, users_get, auth_headers):
        sc, detail = create_user_as_admin(role=passenger_role)
        uid = detail["id"]

        delete = delete_user_by_id(uid, auth_headers)
        assert delete is True, f"Expected user {uid} to be deleted successfully"

        resp = users_get(auth_headers, params={"skip": 0, "limit": 100})
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}. Body: {resp.text}"
        users = resp.json()
        ids = [u["id"] for u in users]
        assert uid not in ids, f"User {uid} was not deleted"

    # Optional: keep this test in case the API contract changes in the future
    # def test_delete_non_existent_user_id_as_admin(self, fake_user_id, auth_headers):
    #     resp = api_request("delete", f"{USERS}{fake_user_id}", headers=auth_headers)
    #     assert resp.status_code == 404, f"Expected 404, got {resp.status_code}. Body: {resp.text}"

    def test_delete_user_without_token(self, create_user_as_admin):
        sc, detail = create_user_as_admin(role=passenger_role)
        uid = detail["id"]

        resp = api_request("delete", f"{USERS}{uid}")
        assert resp.status_code == 401, f"Expected 401, got {resp.status_code}. Body: {resp.text}"
        assert resp.json().get("detail") == "Not authenticated"

    def test_delete_user_with_passenger_token(self, create_user_as_admin, passenger_headers):
        sc, detail = create_user_as_admin(role=passenger_role)
        uid = detail["id"]

        resp = api_request("delete", f"{USERS}{uid}", headers=passenger_headers)
        assert resp.status_code == 403, f"Expected 403, got {resp.status_code}. Body: {resp.text}"
        assert resp.json().get("detail") in ("Admin privileges required", "Forbidden")
