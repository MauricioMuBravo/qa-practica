import os
import re
import pytest
from selenium import webdriver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    resultado = yield
    reporte = resultado.get_result()
    setattr(item, "rep_" + reporte.when, reporte)


@pytest.fixture
def driver(request):
    opciones = webdriver.ChromeOptions()
    opciones.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    opciones.add_argument("--disable-notifications")
    d = webdriver.Chrome(options=opciones)
    yield d
    reporte = getattr(request.node, "rep_call", None)
    if reporte is not None and reporte.failed:
        os.makedirs("capturas", exist_ok=True)
        nombre = re.sub(r"[^\w\-]", "_", request.node.name)
        d.save_screenshot(f"capturas/{nombre}.png")
    d.quit()