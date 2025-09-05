# API/utils/data_users.py

from API.utils.data import *

# ---------- Payloads válidos ----------
valid_update_payload = {
    "email": "updated@example.com",
    "password": valid_password,
    "full_name": valid_full_name,
}

update_role_payload = {
    "email": "updated@example.com",
    "password": valid_password,
    "full_name": valid_full_name,
    "role": admin_role
}

# ---------- Payloads inválidos ----------
invalid_email_payload = {
    "email": "bad",
    "password": valid_password,
    "full_name": valid_full_name,
}

missing_email_payload = {
    "password": valid_password,
    "full_name": valid_full_name
}

missing_password_payload = {
    "email": "someone@example.com",
    "full_name": valid_full_name
}

missing_full_name_payload = {
    "email": "someone@example.com",
    "password": valid_password
}
