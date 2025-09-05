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


# ========== PAGINATION ==========
DEFAULT_PAGE_SIZE = 10

# ========== TAIL NUMBERS ==========

valid_tail_number = "PY-7162A"
min_valid_tail_number = "AR-524"
empty_tail_number = ""
tail_number_with_accents = "ÁR-524"
tail_number_with_apostrophe = "A'R-524"
tail_number_with_space = "AR 524"
below_max_tail_number = "AR-524ARA"
max_tail_number = "AR-524ARAR"
above_max_tail_number = "AR-524ARARA"
symbols_only_tail_number = "@#$%^&*"
unicode_tail_number = "李雷-李雷李雷"
spaces_only_tail_number = "   "

tail_numbers_to_test = [
    {"tail_number": valid_tail_number, "expected_status": 201},
    {"tail_number": min_valid_tail_number, "expected_status": 201},
    {"tail_number": empty_tail_number, "expected_status": 422},
    {"tail_number": tail_number_with_accents, "expected_status": 422},
    {"tail_number": tail_number_with_apostrophe, "expected_status": 422},
    {"tail_number": tail_number_with_space, "expected_status": 201},
    {"tail_number": below_max_tail_number, "expected_status": 201},
    {"tail_number": max_tail_number, "expected_status": 201},
    {"tail_number": above_max_tail_number, "expected_status": 422},
    {"tail_number": symbols_only_tail_number, "expected_status": 422},
    {"tail_number": unicode_tail_number, "expected_status": 422},
    {"tail_number": spaces_only_tail_number, "expected_status": 422},
]

# ========== CAPACITIES ==========

valid_capacity = 200
negative_capacity = -200
zero_capacity = 0
wrong_capacity_type = "abc"

capacities_to_test = [
    {"capacity": valid_capacity, "expected_status": 201},
    {"capacity": negative_capacity, "expected_status": 422},
    {"capacity": zero_capacity, "expected_status": 422},
    {"capacity": wrong_capacity_type, "expected_status": 422},
]

# ========== MODELS ==========

valid_model = "Airbus A320-200"
empty_model = ""

models_to_test = [
    {"model": valid_model, "expected_status": 201},
    {"model": empty_model, "expected_status": 422},
]

aircraft_cases = tail_numbers_to_test + models_to_test + capacities_to_test


# ========== PAGINATION VALUES ==========

pagination_values_to_test = [
    {"skip": 0, "limit":20, "expected_status": 200},
    {"skip": 5, "limit":20, "expected_status": 200},
    {"skip": "abc", "limit":0, "expected_status": 422},
    {"skip": 0, "limit": "abc", "expected_status": 422},
]

# ========== DATE-TIME ==========

valid_date_time = "2025-09-02T18:10:15"
no_t_separator_date_time = "2025-09-0218:10:15"
space_separator_date_time = "2025-09-02 18:10:15"
lower_t_separator_date_time = "2025-09-02t18:10:15"
Z_timezone_date_time = "2025-09-02T18:10:15Z"
A_timezone_date_time = "2025-09-02T18:10:15A"
offset_timezone_date_time = "2025-09-02T18:10:15+2:00"
decimal_seconds_date_time = "2025-09-02T18:10:15.225"
slash_date_time = "2025/09/02T18:10:15"
single_digit_day_date_time = "2025-09-2T18:10:15"

date_time_values_to_test = [
    {"date_time": valid_date_time, "expected_status": 201},
    {"date_time": no_t_separator_date_time, "expected_status": 422},
    {"date_time": space_separator_date_time, "expected_status": 201},
    {"date_time": lower_t_separator_date_time, "expected_status": 201},
    {"date_time": Z_timezone_date_time, "expected_status": 201},
    {"date_time": A_timezone_date_time, "expected_status": 422},
    {"date_time": offset_timezone_date_time, "expected_status": 201},
    {"date_time": decimal_seconds_date_time, "expected_status": 201},
    {"date_time": slash_date_time, "expected_status": 422},
    {"date_time": single_digit_day_date_time, "expected_status": 422},
]

# ========== DATA PARA AIRPORTS =========
# ========== IATA CODE  ========
valid_iata_code = "CDG"
above_limit_iata_code = "CDGZ"
empty_iata_code = ""
below_limit_iata_code = "CD"
lowercase_iata_code = "hnd"
numeric_iata_code = "190"

iata_code_to_test = [
    { "iata_code": valid_iata_code, "expected_status": 201},
    { "iata_code": above_limit_iata_code, "expected_status": 422},
    { "iata_code": empty_iata_code, "expected_status": 422},
    { "iata_code": below_limit_iata_code, "expected_status": 422},
    { "iata_code": lowercase_iata_code, "expected_status": 422},
    { "iata_code": numeric_iata_code, "expected_status": 422}
]

# ========== CITY ==========

valid_city = "Paris"
valid_city_string = "4@r15"
empty_city = ""
type_int_city = 0

city_to_test = [
    {"city": valid_city, "expected_status": 201},
    {"city": valid_city_string, "expected_status": 422}, #esperado 422, aunque el contrato lo permita (acepta datos inválidos), no es válido para negocio
    {"city": empty_city, "expected_status": 422}, #esperado 422, aunque el contrato lo permita (es string), pero no es válido para negocio
    {"city": type_int_city, "expected_status": 422},
]

# ========== COUNTRY ==========

valid_country = "Francia"
valid_country_string = "4R@NC14"
empty_country = ""
type_int_country = 0

country_to_test = [
    {"country": valid_country, "expected_status": 201},
    {"country": valid_country_string, "expected_status": 422},  #esperado 422, aunque el contrato lo permita (acepta datos inválidos), no es válido para negocio
    {"country": empty_country, "expected_status": 422}, #esperado 422, aunque el contrato lo permita (es string), pero no es válido para negocio
    {"country": type_int_country, "expected_status": 422},
]


