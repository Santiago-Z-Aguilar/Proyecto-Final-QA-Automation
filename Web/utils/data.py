
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

# ========== PLP ==========

CATEGORIES = {
    "men": "Men's Clothes",
    "women": "Women's Clothes",
    "electronics": "Electronics",
    "books": "Books",
    "groceries": "Groceries"
}

CATEGORY_DESCRIPTIONS = {
    "Men's Clothes": "Showing 10 of 10 products (Page 1 of 1)",
    "Women's Clothes": "Showing 10 of 10 products (Page 1 of 1)",
    "Electronics": "Showing 10 of 10 products (Page 1 of 1)",
    "Books": "Showing 10 of 10 products (Page 1 of 1)",
    "Groceries": "Showing 10 of 10 products (Page 1 of 1)"
}

CATEGORY_SLUGS = {
    "Men's Clothes": "men-clothes",
    "Women's Clothes": "women-clothes",
    "Electronics": "electronics",
    "Furniture": "furniture",
    "Shoes": "shoes"
}