# tests/auth/data.py
import random
import string
import uuid
from faker import Faker
from datetime import timedelta, datetime
from decimal import Decimal, ROUND_HALF_UP
faker = Faker()

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
    {"skip": None, "limit":None, "expected_status": 200},
    {"skip": 0, "limit":20, "expected_status": 200},
    {"skip": 5, "limit":20, "expected_status": 200},
    {"skip": "abc", "limit":0, "expected_status": 422},
    {"skip": 0, "limit": "abc", "expected_status": 422},
    #{"skip": 99999, "limit": 10, "expected_status": 200}
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

# ========== DATA FLIGHTS ==========
# ========== IATA ==========
chars = [str(faker.random_int(0, 9)), faker.random_uppercase_letter(), faker.random_uppercase_letter()]

valid_iata_origin = ''.join(random.choices(string.ascii_uppercase, k=3))
valid_iata_destination = ''.join(random.choices(string.ascii_uppercase, k=3))
iata_number_letters = ''.join(random.sample(chars, len(chars)))
iata_four_chr = ''.join(random.choices(string.ascii_uppercase, k=4))
iata_two_chr = ''.join(random.choices(string.ascii_uppercase, k=2))
iata_lowercase = ''.join(random.choices(string.ascii_lowercase, k=3))
iata_lower_uppercase = ''.join(random.choices(string.ascii_letters, k=3))
iata_empty = ""

iata_cases = [
    ("origin", valid_iata_origin, 201),
    ("origin", iata_number_letters, 422),
    ("origin", iata_four_chr, 422),
    ("origin", iata_two_chr, 422),
    ("origin", iata_lowercase, 422),
    ("origin", iata_lower_uppercase, 422),
    ("origin", iata_empty, 422),

    ("destination", valid_iata_destination, 201),
    ("destination", iata_number_letters, 422),
    ("destination", iata_four_chr, 422),
    ("destination", iata_two_chr, 422),
    ("destination", iata_lowercase, 422),
    ("destination", iata_lower_uppercase, 422),
    ("destination", iata_empty, 422),
    ("destination", valid_iata_origin, 201),  # ojo: debería fallar por reglas de negocio
]


# ========== DATE TIME ==========
today = datetime.today()
pas = today - timedelta(days=faker.random_int(min=10, max=50))
future = today + timedelta(days=faker.random_int(min=10, max=30))

datetime_today = today.strftime("%Y-%m-%dT%H:%M:%S") + f".{today.microsecond // 1000:03d}Z"
datetime_pass = pas.strftime("%Y-%m-%dT%H:%M:%S")
datetime_future = future.strftime("%Y-%m-%dT%H:%M:%S")
datetime_empty = ""
datetime_zero = 0
datetime_number = faker.random_int(min=1, max=1000)
datetime_slash = today.strftime("%Y/%m/%dT%H:%M:%S.%f")[:-3] + "Z"
datetime_mdy = today.strftime("%m/%d/%YT%H:%M:%S.%f")[:-3] + "Z"
datetime_dmy = today.strftime("%d/%m/%YT%H:%M:%S.%f")[:-3] + "Z"

datetime_cases = [
    ("departure_time", datetime_today, 201),
    ("departure_time", datetime_pass, 422),
    ("departure_time", datetime_future, 201),
    ("departure_time", datetime_empty, 422),
    ("departure_time", datetime_zero, 422),
    ("departure_time", datetime_number, 422),
    ("departure_time", datetime_slash, 422),
    ("departure_time", datetime_mdy, 422),
    ("departure_time", datetime_dmy, 422),

    ("arrival_time", datetime_today, 201),
    ("arrival_time", datetime_pass, 422),
    ("arrival_time", datetime_future, 201),
    ("arrival_time", datetime_empty, 422),
    ("arrival_time", datetime_zero, 422),
    ("arrival_time", datetime_number, 422),
    ("arrival_time", datetime_slash, 422),
    ("arrival_time", datetime_mdy, 422),
    ("arrival_time", datetime_dmy, 422),
]

# ========== BASE PRICE ==========
decimal = Decimal(str(faker.random.uniform(1, 10000))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

base_price_valid = float(decimal)
base_price_int = faker.random_number(digits=24, fix_len=True)
base_price_30digits = faker.random_number(digits=30, fix_len=True)
base_price_negative = -faker.random_number(digits=30, fix_len=True)
base_price_zero = 0
base_price_string = faker.word()

baseprice_cases = [
    {"base_price": base_price_valid, "expected_status": 201},
    {"base_price": base_price_int, "expected_status": 201},
    {"base_price": base_price_30digits, "expected_status": 201},
    {"base_price": base_price_negative, "expected_status": 422},
    {"base_price": base_price_zero, "expected_status": 201},
    {"base_price": base_price_string, "expected_status": 422}
]

# ========== AIRCRAFT ==========
id_aircraft_generated = f"acf-{uuid.uuid4().hex[:8]}"
id_aircraft_empty = ""
id_aircraft_number = faker.random_number(digits=10, fix_len=True)

aircraft_data_to_test = [
    {"aircraft_id": id_aircraft_generated, "expected_status": 422},
    {"aircraft_id": id_aircraft_empty, "expected_status": 422},
    {"aircraft_id": id_aircraft_number, "expected_status": 422}
]

# ========== SEATS ==========
seats_valid = faker.random_int(min=1, max=500)
seats_decimal = Decimal(str(faker.random.uniform(1, 10000))).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
seats_30digits = faker.random_number(digits=30, fix_len=True)
seats_1digit = faker.random_number(digits=1, fix_len=True)
seats_negative = -faker.random_number(digits=30, fix_len=True)
seats_zero = 0
seats_string = faker.word()

seats_cases = [
    {"available_seats": seats_valid, "expected_status": 201},
    {"available_seats": seats_decimal, "expected_status": 422},
    {"available_seats": seats_30digits, "expected_status": 201}, #No deberia
    {"available_seats": seats_1digit, "expected_status": 201},
    {"available_seats": seats_negative, "expected_status": 422},
    {"available_seats": seats_zero, "expected_status": 201},
    {"available_seats": seats_string, "expected_status": 201},
]


# ========== PASSENGERS ==========
valid_passenger = {"full_name": valid_full_name,"passport": "string","seat": "12A"}
null_seat_passenger = {"full_name": valid_full_name,"passport": "string","seat": None}
missing_full_name_passenger = {"passport": "string","seat": "12A"}
missing_passport_passenger = {"full_name": valid_full_name,"seat": "12A"}

one_passenger_payload = [valid_passenger]
two_passengers_payload = [valid_passenger,valid_passenger]
null_seat_payload = [null_seat_passenger]
no_passengers_payload = []
missing_full_name_payload = [missing_full_name_passenger]
missing_passport_payload = [missing_full_name_passenger]

passengers_to_test = [
    {"passengers": one_passenger_payload, "expected_status": 201},
    {"passengers": two_passengers_payload, "expected_status": 201},
    {"passengers": null_seat_payload, "expected_status": 201},
    {"passengers": no_passengers_payload, "expected_status": 422},
    {"passengers": missing_full_name_payload, "expected_status": 422},
    {"passengers": missing_passport_payload, "expected_status": 422}
]

# ========== FLIGHTS ==========

flights_to_test = [
    {"flight_id": id_aircraft_generated, "expected_status": 404},
    {"flight_id": id_aircraft_empty, "expected_status": 404},
    {"flight_id": id_aircraft_number, "expected_status": 422},
    {"flight_id": None, "expected_status": 422},
]


