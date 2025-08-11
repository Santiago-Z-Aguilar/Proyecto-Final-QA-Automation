













# import uuid
# import pytest
# import time
# from faker import Faker
# from utils.settings import USERS
# from utils.api_helpers import api_request
#
# fake = Faker()
#
#
# def delete_user_by_email(email: str, auth_headers) -> bool:
#     """
#     Busca usuarios con el email dado y elimina cada uno encontrado.
#     Retorna True si todos fueron eliminados exitosamente, False si falló o no encontró.
#     """
#     # Obtener todos los usuarios para buscar el id del que tenga el email
#     response = api_request("get", USERS, headers=auth_headers)
#     if response is None or response.status_code != 200:
#         print(f"❌ No se pudo obtener la lista de usuarios para eliminar email {email}")
#         return False
#
#     users = response.json()
#     # Filtrar usuarios con el email dado (normalmente solo uno)
#     users_to_delete = [u for u in users if u.get("email") == email]
#
#     if not users_to_delete:
#         print(f"ℹ️ No se encontró usuario con email {email} para eliminar.")
#         return True  # No hay usuario, está limpio
#
#     all_deleted = True
#     for user in users_to_delete:
#         user_id = user.get("id")
#         if not user_id:
#             continue
#
#         del_response = api_request("delete", f"{USERS}{user_id}", headers=auth_headers)
#         if del_response is None or del_response.status_code != 204:
#             print(f"⚠️ Falló eliminar usuario {email} (ID: {user_id}), status: {del_response.status_code if del_response else 'None'}")
#             all_deleted = False
#             continue
#
#         # Esperar a que se confirme la eliminación
#         if not wait_until_user_deleted(user_id, auth_headers):
#             print(f"❌ Usuario {email} (ID: {user_id}) sigue existiendo tras varios intentos.")
#             all_deleted = False
#
#     return all_deleted
#
#
#
#
# @pytest.fixture
# def create_user():
#     def _create_user(auth_headers, role="admin"):
#         email = f"test_{uuid.uuid4()}@example.com"
#
#         # Limpieza previa para evitar conflicto
#         delete_user_by_email(email, auth_headers)
#
#         user_data = {
#             "email": email,
#             "password": "Test1234!",
#             "full_name": "Artya2",
#             "role": role
#         }
#
#         print(f"📤 Attempt to create user with email: {user_data['email']}")
#         response = api_request(
#             "post",
#             USERS,
#             headers=auth_headers,
#             json=user_data,
#             retry_400=True
#         )
#
#         if response is None:
#             raise Exception("❌ No se pudo crear el usuario después de varios intentos.")
#
#         if response.status_code >= 400:
#             print(f"❌ Error al crear usuario: {response.status_code} - {response.text}")
#             raise Exception(f"❌ Error al crear usuario. Status: {response.status_code}")
#
#         return response.json()
#
#     return _create_user
#
#
# @pytest.fixture
# def user_fixture(request, auth_headers, create_user):
#     role = getattr(request, "param", "admin")
#     user = create_user(auth_headers, role)
#     yield user
#
#     # Intentar eliminar usuario
#     try:
#         delete_response = api_request("delete", f"{USERS}{user['id']}", headers=auth_headers)
#         if delete_response and delete_response.status_code == 204:
#             print(f"✅ User deleted: {user['email']}")
#
#             # Confirmar que el usuario fue eliminado realmente
#             if not wait_until_user_deleted(user['id'], auth_headers):
#                 print(f"❌ Usuario {user['email']} sigue existiendo después de varios intentos.")
#         else:
#             print(
#                 f"⚠️ Falló eliminar usuario {user['email']} (Status: {delete_response.status_code if delete_response else 'no response'})")
#     except Exception as e:
#         print(f"❌ Exception durante eliminación de usuario: {e}")
#
#
# def wait_until_user_deleted(user_id, auth_headers, max_attempts=5, wait_seconds=1):
#     for attempt in range(max_attempts):
#         response = api_request("get", f"{USERS}{user_id}", headers=auth_headers)
#         if response.status_code == 404:
#             return True
#         print(f"⚠️ Usuario todavía existe (intento {attempt + 1}/{max_attempts}), esperando {wait_seconds}s...")
#         time.sleep(wait_seconds)
#     return False
