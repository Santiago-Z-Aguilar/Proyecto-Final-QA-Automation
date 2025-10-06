import pytest
from Web.pages.banner_slider_page import BannerSliderPage
from Web.pages.home_page import HomePage
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.slider
def test_slider_is_moving_auto(driver):
    home = HomePage(driver)
    home.load()
    slider = BannerSliderPage(driver)

    first_src = slider.get_active_slide_src()
    slider.click_next()
    second_src = slider.get_active_slide_src()
    assert first_src != second_src, f"Slide 2 no cambió (src={second_src})"

    slider.click_next()
    third_src = slider.get_active_slide_src()
    assert third_src not in [first_src, second_src], f"Slide 3 no se mostró correctamente (src={third_src})"

    slider.click_prev()
    back_to_second_src = slider.get_active_slide_src()
    assert back_to_second_src == second_src, f"No regresó al slide 2 (esperado {second_src}, obtenido {back_to_second_src})"


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


@pytest.mark.slider
def test_shop_now_redirect(driver):
    """Validate that button 'Shop Now' redirects to Clothes (It fails)"""
    home = HomePage(driver)
    home.load()
    slider = BannerSliderPage(driver)

    btn = slider.get_active_slide_button()
    assert btn.text.strip() == "Shop Now"

    slider.save_slider_screenshot("slide1_shop_now_before_click")
    slider.driver.execute_script("arguments[0].click();", btn)

    expected_url = "https://shophub-commerce.vercel.app/categories/men-clothes"

    try:
        WebDriverWait(slider.driver, 5).until(lambda d: d.current_url == expected_url)
    except Exception:
        slider.save_slider_screenshot("slide1_shop_now_redirect_fail")

    actual_url = slider.driver.current_url
    assert actual_url == expected_url, f"Shop Now expected {expected_url}, got {actual_url}"


@pytest.mark.slider
def test_explore_redirect(driver):
    """Validate that button 'Explore' redirects to Electronics (It fails)"""
    home = HomePage(driver)
    home.load()
    slider = BannerSliderPage(driver)

    slider.click_next()  # Ir al segundo slide
    btn = slider.get_active_slide_button()
    assert btn.text.strip() == "Explore"

    slider.save_slider_screenshot("slide2_explore_before_click")
    slider.driver.execute_script("arguments[0].click();", btn)

    expected_url = "https://shophub-commerce.vercel.app/categories/electronics"

    try:
        # Espera corta, porque sabemos que fallará
        WebDriverWait(slider.driver, 5).until(lambda d: d.current_url == expected_url)
    except Exception:
        # Capturamos screenshot del fallo
        slider.save_slider_screenshot("slide2_explore_redirect_fail")

    # Validación final para marcar el test como fallido
    actual_url = slider.driver.current_url
    assert actual_url == expected_url, (
        f"Explore expected {expected_url}, got {actual_url} (fallo esperado)"
    )


@pytest.mark.slider
def test_order_now_redirect(driver):
    """Validate that button 'Order Now' redirects to Groceries"""
    home = HomePage(driver)
    home.load()
    slider = BannerSliderPage(driver)

    slider.click_next()  # Segundo slide
    slider.click_next()  # Tercer slide
    btn = slider.get_active_slide_button()
    assert btn.text.strip() == "Order Now"

    slider.save_slider_screenshot("slide3_order_now_before_click")
    slider.driver.execute_script("arguments[0].click();", btn)

    expected_url = "https://shophub-commerce.vercel.app/categories/groceries"
    WebDriverWait(slider.driver, 10).until(lambda d: d.current_url == expected_url)
    slider.save_slider_screenshot("slide3_order_now_after_click")
    assert slider.driver.current_url == expected_url