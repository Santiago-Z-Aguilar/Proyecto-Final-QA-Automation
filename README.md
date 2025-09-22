# 🧪 QA Automation - CF Final Project

This repository contains the **final automation project** for the *Automation Testing Bootcamp* by Código Facilito.  
It includes automated tests for both the **Airlines API** and the **ShopHub Web application**, built with **Python, Pytest, Selenium, and Requests**.  

> 📌 *For the Spanish version of this README, scroll down.*

---

## 📂 Project Structure

```
.
├── API
│   ├── tests/           # API test cases (auth, users, bookings, aircrafts, airports, flights)
│   └── utils/           # API helpers and shared functions
├── Web
│   ├── locators/        # Page locators for UI elements
│   ├── pages/           # Page Object Model (POM) classes
│   ├── test_data/       # Test data for Web tests
│   ├── tests/           # Web test cases
│   └── utils/           # Web utilities (driver factory, config)
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Santiago-Z-Aguilar/Proyecto-Final-QA-Automation
   cd Proyecto-Final-QA-Automation
   ```

2. **(Recommended)** Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the Tests

### API Tests (online)

⚠️ **Important**: The Airlines API hosted on Render is fragile with high concurrency.
For stable execution, use **4 workers or less and `--dist=loadscope`**:

```bash
pytest -n4 --dist=loadscope API/tests
```

Running with more workers may cause unexpected API errors.

---

### API Tests (local option)

If you want to run the Airlines API locally, follow the setup instructions in this repository:
👉 [cf-automation-airline-api](https://github.com/terranigmark/cf-automation-airline-api)

Once running, update the `BASE_URL` in:

```
API/utils/settings.py
```

to match your local API URL.

---

### Web Tests

ShopHub Web tests can run with more workers. Recommended:

```bash
pytest -n auto --dist=loadscope Web/tests
```

---

## 📦 Tech Stack

* **Language:** Python 3.12+
* **Frameworks & Tools:** Pytest, Selenium, Requests, Webdriver-Manager, Pytest-xdist, Pytest-bdd, Pytest-html
* **Approach:** Page Object Model (POM), Fixtures, HTML Reports, Equivalence Classes, Boundary Testing

---

## 👥 Team & Contributions

### Santiago Gonzalez Aguilar — [Santiago-Z-Aguilar](https://github.com/Santiago-Z-Aguilar)

* Automated API tests for *Aircrafts* and *Bookings*
* Automated Web tests for the *Checkout* flow
* Implemented GitHub Actions pipeline for CI/CD

---

### Yamilet Rivera — [yamiletriveraqa](https://github.com/yamiletriveraqa)

* Designed Web test matrix for positive cases (Logo, Menu, Search, Sign Up, Login, Banner, PLP, PDP, Cart, Checkout, Thank You Page)
* Automated Web tests for *Login* and *Product List Page (PLP)*
* Designed and automated API tests for the *Airports*

---

### Alisson Pineda — [AlissonPineda13](https://github.com/AlissonPineda13)

* Documented Web test matrix (Logo, Menu, Login, Sign Up, Search Bar, Banner Slider, Recommended Products, Product Page, Cart, Checkout)
* Created test cases for *Flights* (all methods) and *DELETE Aircraft*
* Automated API tests for the *Flights* endpoint
* Automated Web tests for key user flows:

  * **Logo**
  * **Sign Up**
  * **Search**
  * **Slider Banner**

---

### Josué Tenorio — [JosueTenorio99](https://github.com/JosueTenorio99)

* Created API test matrices for *Auth, Users, and Bookings* endpoints
* Designed boundary value and equivalence class tests for ShopHub Web
* Automated API tests for *Auth* and *Users*
* Automated Web tests for *Product Detail Page* and *Shopping Cart*

---

## 🙌 Acknowledgments

Special thanks to our teachers at Código Facilito for their guidance:
**Héctor Vega, Yuliana Alvarez, Anely Doporto Valladares, and David C.**

---

# 🧪 QA Automation - CF Final Project (Español)

Este repositorio contiene el **proyecto final de automatización** del *Bootcamp de Testing Automatizado* de Código Facilito.
Incluye pruebas automatizadas para la **API Airlines** y la **aplicación Web ShopHub**, desarrolladas con **Python, Pytest, Selenium y Requests**.

---

## 📂 Estructura del Proyecto

```
.
├── API
│   ├── tests/           # Casos de prueba para API (auth, users, bookings, aircrafts, airports, flights)
│   └── utils/           # Helpers y funciones compartidas de API
├── Web
│   ├── locators/        # Localizadores de elementos
│   ├── pages/           # Clases Page Object Model (POM)
│   ├── test_data/       # Datos de prueba Web
│   ├── tests/           # Casos de prueba Web
│   └── utils/           # Utilidades (driver factory, config)
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Santiago-Z-Aguilar/Proyecto-Final-QA-Automation
   cd Proyecto-Final-QA-Automation
   ```

2. **(Recomendado)** Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Ejecución de Pruebas

### API (online)

⚠️ **Importante**: La API de Airlines en Render es sensible con concurrencia alta.
Usar **4 workers y `--dist=loadscope`**:

```bash
pytest -n4 --dist=loadscope API/tests
```

Con más workers puede romperse y arrojar errores inesperados.

---

### API (local)

Si quieres correr la API en tu máquina, sigue las instrucciones en:
👉 [cf-automation-airline-api](https://github.com/terranigmark/cf-automation-airline-api)

Luego cambia la variable `BASE_URL` en:

```
API/utils/settings.py
```

por la URL de tu API local.

---

### Web

Las pruebas de ShopHub Web pueden correr con más workers. Recomendado:

```bash
pytest -n auto --dist=loadscope Web/tests
```

---

## 📦 Tecnologías Usadas

* **Lenguaje:** Python 3.12+
* **Frameworks y Herramientas:** Pytest, Selenium, Requests, Webdriver-Manager, Pytest-xdist, Pytest-bdd, Pytest-html
* **Enfoque:** Page Object Model (POM), Fixtures, Reportes HTML, Clases de Equivalencia, Valores Límite

---

## 👥 Equipo y Contribuciones

### Santiago Gonzalez Aguilar — [Santiago-Z-Aguilar](https://github.com/Santiago-Z-Aguilar)

* Automatización API: *Aircrafts* y *Bookings*
* Automatización Web: *Checkout*
* Pipeline de GitHub Actions

---

### Yamilet Rivera — [yamiletriveraqa](https://github.com/yamiletriveraqa)

* Diseño de matriz de casos de prueba Web (Logo, Menú, Search, Sign Up, Login, Banner, PLP, PDP, Carrito, Checkout, Thank You Page)
* Automatización Web: *Login* y *PLP*
* Diseño y automatización API: *Airports*

---

### Alisson Pineda — [AlissonPineda13](https://github.com/AlissonPineda13)

* Documentación de matriz de pruebas Web (Logo, Menú, Login, Sign Up, Barra de Búsqueda, Banner, Productos Recomendados, Página de Producto, Carrito, Checkout)
* Creación de casos de prueba API: *Flights* (todos los métodos) y *DELETE Aircraft*
* Automatización API: *Flights*
* Automatización Web en flujos clave:

  * **Logo**
  * **Sign Up**
  * **Search**
  * **Slider Banner**

---

### Josué Tenorio — [JosueTenorio99](https://github.com/JosueTenorio99)

* Matriz de pruebas API: *Auth, Users, Bookings*
* Casos de prueba: valores límite y clases de equivalencia para ShopHub Web
* Automatización API: *Auth y Users*
* Automatización Web: *Product Detail Page* y *Shopping Cart*

---

## 🙌 Agradecimientos

Un agradecimiento especial a nuestros profesores de Código Facilito por su guía y apoyo:
**Héctor Vega, Yuliana Alvarez, Anely Doporto Valladares y David C.**