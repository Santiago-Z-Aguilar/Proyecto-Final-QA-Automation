from selenium import webdriver

def before_all(context):
    # Configuración de navegador (puedes parametrizarlo igual que en pytest)
    browser = context.config.userdata.get("browser", "chrome").lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        context.driver = webdriver.Chrome(options=options)

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--inprivate")
        context.driver = webdriver.Edge(options=options)

    else:
        raise ValueError(f"Browser not supported: {browser}")

    context.driver.implicitly_wait(10)


def after_all(context):
    # Cerrar el navegador después de todos los tests
    if hasattr(context, "driver"):
        context.driver.quit()


# To run in edge use in terminal -> behave -D browser=edge `
# To run in Chrome use in terminal -> behave Web/tests/features
