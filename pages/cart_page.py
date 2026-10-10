from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    ARTICULOS = (By.CLASS_NAME, "cart_item")

    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, 10)

    def _css(self, selector):
        return (By.CSS_SELECTOR, selector)

    def cantidad_articulos(self):
        self.espera.until(EC.presence_of_all_elements_located(self.ARTICULOS))
        return len(self.driver.find_elements(*self.ARTICULOS))

    def pagar(self, nombre, apellido, codigo_postal):
        self.espera.until(EC.element_to_be_clickable(self._css("[data-test='checkout']"))).click()
        self.espera.until(EC.visibility_of_element_located(self._css("[data-test='firstName']"))).send_keys(nombre)
        self.driver.find_element(*self._css("[data-test='lastName']")).send_keys(apellido)
        self.driver.find_element(*self._css("[data-test='postalCode']")).send_keys(codigo_postal)
        self.espera.until(EC.element_to_be_clickable(self._css("[data-test='continue']"))).click()

    def subtotal(self):
        etiqueta = self.espera.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "summary_subtotal_label"))
        ).text
        return float(etiqueta.split("$")[1])

    def finalizar(self):
        self.espera.until(EC.element_to_be_clickable(self._css("[data-test='finish']"))).click()
        return self.espera.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text
