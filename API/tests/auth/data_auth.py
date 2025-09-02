from API.utils.data import *

emails_to_test_signup = {
    valid_email: 201,
    empty_email: 422,
    below_max_email: 201,
    max_email: 201,
    above_max_email: 422,
    email_with_special_characters: 201,
    email_with_missing_domain: 422,
    email_with_invalid_tld: 422,
    unicode_characters_email: 422,
    unicode_in_domain: 422,
}
passwords_to_test_signup = {
    valid_password: 201,
    min_valid_password: 201,
    below_min_password: 422,
    typical_password_1: 201,
    typical_password_2: 201,
    below_max_password: 422,
    max_password: 422,
    above_max_password: 422,
    numbers_only_password: 201,
    special_characters_password: 201,
    unicode_characters_password: 201,
    password_with_space: 201,
}
raw_full_names_signup = [
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


def normalize_name(name):
    """
    Elimina espacios al inicio y final, y reduce espacios internos a uno solo.
    Si name es None o vacío, lo retorna igual.
    """
    if not name or not isinstance(name, str):
        return name
    return ' '.join(name.strip().split())


full_names_to_test_signup = [
    {
        **item,
        "expected_user_created": normalize_name(item["full_name"])
        if item["expected_status"] == 201
        else None
    }
    for item in raw_full_names_signup
]
