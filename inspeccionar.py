import re
from appium import webdriver
from appium.options.android import UiAutomator2Options


opciones = UiAutomator2Options()
opciones.platform_name = "Android"
opciones.automation_name = "UiAutomator2"
opciones.device_name = "emulator-5554"
opciones.app_package = "com.android.settings"
opciones.app_activity = ".Settings"
opciones.no_reset = True

driver = webdriver.Remote("http://127.0.0.1:4723", options=opciones)
try:
    fuente = driver.page_source
    ids = sorted(set(re.findall(r'resource-id="([^"]+)"', fuente)))
    textos = sorted(set(re.findall(r' text="([^"]+)"', fuente)))
    print("\n=== resource-id ===")
    for i in ids:
        print(i)
    print("\n=== textos visibles ===")
    for t in textos:
        print(t)
finally:
    driver.quit()
