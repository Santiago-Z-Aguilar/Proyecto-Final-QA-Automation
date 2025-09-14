import os
import time
import pytest
from Web.pages.home_page import HomePage
from Web.pages.banner_slider_page import BannerSliderPage
from selenium.webdriver.support.ui import WebDriverWait
from Web.locators.banner_slider_locators import BannerSliderLocators
from selenium.webdriver.common.by import By
from Web.utils.config import Config


@pytest.mark.slider
def test_slider_is_moving_auto(driver):
    home = HomePage(driver)
    home.load()

    slider = BannerSliderPage(driver)

    # --- Slide 1 ---
    first_slide = slider.wait_for_first_slide()
    first_src = first_slide.get_attribute("src")

    # --- Ir a Slide 2 ---
    slider.click_next()
    second_src = slider.get_slide_src(slider.locators.SECOND_SLIDE)
    assert first_src != second_src, f"No cambió al segundo slide, sigue mostrando el primero {second_src}"

    # --- Ir a Slide 3 ---
    slider.click_next()
    third_src = slider.get_slide_src(slider.locators.THIRD_SLIDE)
    assert third_src not in [first_src, second_src], "El tercer slide no se mostró correctamente"

    # --- Volver a Slide 2 ---
    slider.click_previous()
    back_to_second_src = slider.get_slide_src(slider.locators.SECOND_SLIDE)
    assert back_to_second_src == second_src, (
        f"No regresó al segundo slide. Esperado: {second_src}, Obtenido: {back_to_second_src}"
    )


@pytest.mark.slider
def test_slider_navigation_with_arrows(driver):
    home = HomePage(driver)
    home.load()

    slider = BannerSliderPage(driver)

    # --- Slide 1 (activo inicial) ---
    first_src = slider.get_active_slide_src()

    try:
        # --- Next (ir a slide 2) ---
        slider.click_next()
        second_src = slider.get_active_slide_src()
        assert first_src != second_src, f"❌ El slide no cambió al hacer click en Next (sigue en {first_src})"
    except AssertionError as e:
        save_slider_screenshot(driver, "fail_next_to_slide2")
        raise e

    try:
        # --- Next (ir a slide 3) ---
        slider.click_next()
        third_src = slider.get_active_slide_src()
        assert third_src not in [first_src, second_src], f"❌ El slide 3 no se mostró correctamente (src={third_src})"
    except AssertionError as e:
        save_slider_screenshot(driver, "fail_next_to_slide3")
        raise e

    try:
        # --- Prev (volver al slide 2) ---
        slider.click_prev()
        back_to_second_src = slider.get_active_slide_src()
        assert back_to_second_src == second_src, f"❌ No regresó al segundo slide con Prev (esperado {second_src}, obtuvo {back_to_second_src})"
    except AssertionError as e:
        save_slider_screenshot(driver, "fail_prev_to_slide2")
        raise e


@pytest.mark.slider
def save_screenshot(driver, name):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join("screenshots", f"{name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"📸 Screenshot guardado: {path}")

@pytest.mark.slider
def test_slider_dots_navigation(driver):
    home = HomePage(driver)
    home.load()

    slider = BannerSliderPage(driver)

    try:
        # 1. Esperar a que el primer dot esté activo (sin /50 en class)
        WebDriverWait(driver, 10).until(
            lambda d: "bg-white/50" not in slider.get_dots()[0].get_attribute("class")
        )

        initial_active_index = slider.get_active_dot_index()
        assert initial_active_index == 0, (
            f"Se esperaba que el primer dot fuera el activo, pero está activo el {initial_active_index}"
        )

        # 2. Clic en el segundo dot
        slider.click_dot(1)
        new_active_index = slider.get_active_dot_index()
        assert new_active_index == 1, f"El segundo dot no se activó correctamente (activo={new_active_index})"

        # 3. Clic en el tercer dot
        slider.click_dot(2)
        third_active_index = slider.get_active_dot_index()
        assert third_active_index == 2, f"El tercer dot no se activó correctamente (activo={third_active_index})"

        # 4. Validación final: asegurarse que los dots realmente cambian
        assert initial_active_index != new_active_index != third_active_index, (
            f"Los dots no cambiaron correctamente: inicial={initial_active_index}, "
            f"después de segundo={new_active_index}, después de tercero={third_active_index}"
        )

    except Exception as e:
        save_screenshot(driver, "slider_dots_fail")
        raise  # relanza la excepción para que pytest marque fallo

