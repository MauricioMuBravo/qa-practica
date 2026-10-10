from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    URL = "https://www.saucedemo.com"
    USUARIO = (By.ID, "user-name")
    CLAVE = (By.ID, "password")
    BOTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, 10)

    def abrir(self):
        self.driver.get(self.URL)
        return self

    def iniciar_sesion(self, usuario, clave):
        self.driver.find_element(*self.USUARIO).send_keys(usuario)
        self.driver.find_element(*self.CLAVE).send_keys(clave)
        self.driver.find_element(*self.BOTON).click()

    def texto_error(self):
        return self.espera.until(EC.visibility_of_element_located(self.ERROR)).text
