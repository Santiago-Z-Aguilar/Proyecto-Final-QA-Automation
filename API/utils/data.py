# tests/auth/data.py

# ========== CHARACTERS ==========

characters_63 = "a" * 63
characters_64 = "a" * 64
characters_65 = "a" * 65

# ========== EMAILS ==========

VALID_DOMAIN = "@example.com"
passenger_user_token_email = f"passenger_token_jasy{VALID_DOMAIN}"
DEFAULT_EMAIL1 = f"test1jasy{VALID_DOMAIN}"
DEFAULT_EMAIL2 = f"test2jasy{VALID_DOMAIN}"

valid_email = f"test{VALID_DOMAIN}"
empty_email = ""
below_max_email = f"{characters_63}{VALID_DOMAIN}"
max_email = f"{characters_64}{VALID_DOMAIN}"
above_max_email = f"{characters_65}{VALID_DOMAIN}"
email_with_special_characters = "valid.user-123@mail-domain.com"
email_with_missing_domain = "plainaddress"
email_with_invalid_tld = "user@mail.c"
unicode_characters_email = "用户@例子.公司"
unicode_in_domain = "user@exámple.com"
invalid_email = "not-an-email"

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


# ========== FULL NAMES ==========

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

# ========== ROLES ==========

passenger_role = "passenger"
admin_role = "admin"
invalid_role = "invalid_role"
