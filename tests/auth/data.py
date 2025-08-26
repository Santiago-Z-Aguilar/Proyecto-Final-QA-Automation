# tests/auth/data.py

# ========== EMAILS ==========
valid_domain = "@example.com"
DEFAULT_EMAIL1 = f"test1{valid_domain}"
DEFAULT_EMAIL2 = f"test2{valid_domain}"
characters_63 = "a" * 63
characters_64 = "a" * 64
characters_65 = "a" * 65
valid_email = f"test{valid_domain}"
empty_email = ""
below_max_email = f"{characters_63}{valid_domain}"
max_email = f"{characters_64}{valid_domain}"
above_max_email = f"{characters_65}{valid_domain}"
email_with_special_characters = "valid.user-123@mail-domain.com"
email_with_missing_domain = "plainaddress"
email_with_invalid_tld = "user@mail.c"
unicode_characters_email = "用户@例子.公司"
unicode_in_domain = "user@exámple.com"

emails_to_test = [
    {"email": valid_email, "expected_status": 201},
    {"email": empty_email, "expected_status": 422},
    {"email": below_max_email, "expected_status": 201},
    {"email": max_email, "expected_status": 201},
    {"email": above_max_email, "expected_status": 422},
    {"email": email_with_special_characters, "expected_status": 201},
    {"email": email_with_missing_domain, "expected_status": 422},
    {"email": email_with_invalid_tld, "expected_status": 422},
    {"email": unicode_characters_email, "expected_status": 422},
    {"email": unicode_in_domain, "expected_status": 422},
]

# ========== PASSWORDS ==========
valid_password = "P@ssw0rd"
min_valid_password = "abcdef"
below_min_password = "abcde"
typical_password_1 = "Abc123$%"
typical_password_2 = "Abcdefghijk1$"
below_max_password = "a" * 4095
max_password = "a" * 4096
above_max_password = "a" * 8192
numbers_only_password = "1234567890"
special_characters_password = "!@#$%^&*()_+"
unicode_characters_password = "áéíóúüñ¿¡"
password_with_space = "abc 123"

passwords_to_test = [
    {"password": valid_password, "expected_status": 201},
    {"password": min_valid_password, "expected_status": 201},
    {"password": below_min_password, "expected_status": 422},
    {"password": typical_password_1, "expected_status": 201},
    {"password": typical_password_2, "expected_status": 201},
    {"password": below_max_password, "expected_status": 422},
    {"password": max_password, "expected_status": 422},
    {"password": above_max_password, "expected_status": 422},
    {"password": numbers_only_password, "expected_status": 201},
    {"password": special_characters_password, "expected_status": 201},
    {"password": unicode_characters_password, "expected_status": 201},
    {"password": password_with_space, "expected_status": 201},
]

# ========== FULL NAMES ==========
def normalize_name(name):
    """
    Elimina espacios al inicio y final, y reduce espacios internos a uno solo.
    Si name es None o vacío, lo retorna igual.
    """
    if not name or not isinstance(name, str):
        return name
    return ' '.join(name.strip().split())

valid_full_name = "Test Jasy"
min_valid_full_name = "A"
empty_full_name = ""
name_with_accents = "José Pérez"
name_with_apostrophe = "O'Connor"
name_with_space = "Anna Maria"
below_max_full_name = "a" * 4095
max_full_name = "a" * 4096
above_max_full_name = "a" * 8192
alphanumeric_full_name = "Anna123"
symbols_only_full_name = "@#$%^&*"
unicode_full_name = "李雷"
unicode_letters_with_spaces = "José Hernández"
leading_space_full_name = " Anna"
trailing_space_full_name = "Anna "
multiple_spaces_full_name = "Anna   Maria"
spaces_only_full_name = "   "
leading_and_trailing_spaces = "   Anna   Maria   "
name_with_spaces_end = " Anna   "

raw_full_names = [
    {"full_name": valid_full_name, "expected_status": 201},
    {"full_name": min_valid_full_name, "expected_status": 201},
    {"full_name": empty_full_name, "expected_status": 422},
    {"full_name": spaces_only_full_name, "expected_status": 422},
    {"full_name": name_with_accents, "expected_status": 201},
    {"full_name": name_with_apostrophe, "expected_status": 201},
    {"full_name": name_with_space, "expected_status": 201},
    {"full_name": below_max_full_name, "expected_status": 422},
    {"full_name": max_full_name, "expected_status": 422},
    {"full_name": above_max_full_name, "expected_status": 422},
    {"full_name": alphanumeric_full_name, "expected_status": 422},
    {"full_name": symbols_only_full_name, "expected_status": 422},
    {"full_name": unicode_full_name, "expected_status": 201},
    {"full_name": unicode_letters_with_spaces, "expected_status": 201},
    {"full_name": leading_space_full_name, "expected_status": 201, "test_case": "trimming"},
    {"full_name": trailing_space_full_name, "expected_status": 201, "test_case": "trimming"},
    {"full_name": multiple_spaces_full_name, "expected_status": 201, "test_case": "trimming"},
    {"full_name": leading_and_trailing_spaces, "expected_status": 201, "test_case": "trimming"},
    {"full_name": name_with_spaces_end, "expected_status": 201, "test_case": "trimming"},
]

full_names_to_test = [
    {
        **item,
        "expected_user_created": normalize_name(item["full_name"])
        if item["expected_status"] == 201
        else None
    }
    for item in raw_full_names
]

