import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    opciones = UiAutomator2Options()
    opciones.platform_name = "Android"
    opciones.automation_name = "UiAutomator2"
    opciones.device_name = "emulator-5554"
    opciones.no_reset = True
    d = webdriver.Remote("http://127.0.0.1:4723", options=opciones)
    yield d
    d.quit()


def texto(valor):
    return (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{valor}")')


def test_pantalla_de_inicio_muestra_apps(driver):
    driver.press_keycode(3)  # botón Home
    espera = WebDriverWait(driver, 15)
    for app in ["Chrome", "Gmail", "Messages"]:
        elemento = espera.until(EC.presence_of_element_located(texto(app)))
        assert elemento.is_displayed(), f"No se ve {app}"


def test_abrir_ajustes(driver):
    driver.activate_app("com.android.settings")
    espera = WebDriverWait(driver, 20)
    espera.until(lambda d: d.current_package == "com.android.settings")
    assert driver.current_package == "com.android.settings"
