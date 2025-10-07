
VALID_USER_LOGIN = [
    {"email": "ana.garcia@gmail.com", "password": "Ana2024!"},
    {"email": "ANA.GARCIA@GMAIL.COM", "password": "Ana2024!"}
]

INVALID_USER_LOGIN = [
    {"email": "ana.garcia@gmail.com", "password": "1"}, #password inválido
    {"email": "", "password": ""}, #campos vacíos
    {"email": "ag@.com", "password": "5"}, #email con formato inválido
    {"email": "yami30@gmail.com", "password": "12345"} #email no registrado
]


VALID_USER_SIGNUP = [
    {
        "firstname": "Ana",
        "lastname": "Garcia",
        "email": "ana.garcia@gmail.com",
        "zipcode": 90210,
        "password": "Ana2024!"
    },
    {
        "firstname": "Ana",
        "lastname": "Garcia",
        "email": "ana.garcia@gmail.com",
        "zipcode": 90210,
        "password": 1
    }
]

INVALID_USER_SIGNUP = [
    {
        "firstname": "Ana",
        "lastname": "Garcia",
        "email": "ana.garcia@gmail.com", #Email already registered
        "zipcode": 90210,
        "password": "Ana2024!"
    },
    {
        "firstname": 12345, #Numbers as name
        "lastname": 67890,  #Numbers as lastname
        "email": "numbername@mail.com",
        "zipcode": 90210,
        "password": "Juan#123"
    },
    {
        "firstname": "Juan",
        "lastname": "López",
        "email": "", #Empty email
        "zipcode": 90210,
        "password": "Juan#123"
    },
    {
        "firstname": "Juan",
        "lastname": "López",
        "email": "juan.lopez@gmail.com",
        "zipcode": "text", #Strings as zipcode
        "password": "Juan#123"
    },
    {
        "firstname": "Juan",
        "lastname": "López",
        "email": "invalidemail",  #Invalid email format
        "zipcode": 90210,
        "password": "Juan#123"
    },
    {
        "firstname": "Juan",
        "lastname": "López",
        "email": "nodomain@.com",  #email without domain
        "zipcode": 90210,
        "password": "Juan#123"
    },
    {
        "firstname": "", #Empty credentials
        "lastname": "",
        "email": "",
        "zipcode": "",
        "password": ""
    },
    {
        "firstname": 12345, #all invalid credentials
        "lastname": 67890,
        "email": "invalid@none",
        "zipcode": "abcd",
        "password": 123
    }
]
# CHECKOUT DATA

VALID_USER_CHECKOUT =     {
        "firstname": "Juan",
        "lastname": "López",
        "email": "juan.perez@test.com",
        "phone": 5551234567,
        "address": "Av. Reforma 123",
        "city": "CDMX",
        "zipcode": 12345,
        "country": "Mexico"
    }

INCOMPLETE_EMAIL_USER_CHECKOUT1 =     {
        **VALID_USER_CHECKOUT,
        "email": "juan@.com"
    }
INCOMPLETE_EMAIL_USER_CHECKOUT2 =     {
    **VALID_USER_CHECKOUT,
    "email": "@abc.com"
    }
INCOMPLETE_EMAIL_USER_CHECKOUT3 =     {
    **VALID_USER_CHECKOUT,
    "email": "juan@abc"
    }


USER_CHECKOUT_FIELDS = ["firstname", "lastname", "email", "phone", "address", "city", "zipcode", "country"]

INCOMPLETE_EMAIL_USERS = [INCOMPLETE_EMAIL_USER_CHECKOUT1, INCOMPLETE_EMAIL_USER_CHECKOUT2,INCOMPLETE_EMAIL_USER_CHECKOUT3]
