from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    TITULO = (By.CLASS_NAME, "title")
    CARRITO = (By.CLASS_NAME, "shopping_cart_link")
    INSIGNIA = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver):
        self.driver = driver
        self.espera = WebDriverWait(driver, 10)

    def titulo(self):
        return self.espera.until(EC.visibility_of_element_located(self.TITULO)).text

    def agregar_producto(self, id_producto):
        boton = (By.CSS_SELECTOR, f"[data-test='add-to-cart-{id_producto}']")
        self.espera.until(EC.element_to_be_clickable(boton)).click()

    def cantidad_en_carrito(self):
        return int(self.espera.until(EC.visibility_of_element_located(self.INSIGNIA)).text)

    def abrir_carrito(self):
        self.espera.until(EC.element_to_be_clickable(self.CARRITO)).click()
