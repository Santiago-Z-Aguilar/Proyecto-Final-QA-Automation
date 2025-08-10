# utils/user_helpers.py

import logging
import time
from utils.api_helpers import api_request, RETRIES, DELAY
from utils.settings import USERS, AUTH_SIGN_UP

logger = logging.getLogger("qa_tests")

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
