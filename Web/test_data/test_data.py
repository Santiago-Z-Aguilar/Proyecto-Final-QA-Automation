
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
