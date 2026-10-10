from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def test_compra_completa(driver):
    LoginPage(driver).abrir().iniciar_sesion("standard_user", "secret_sauce")

    inventario = InventoryPage(driver)
    inventario.agregar_producto("sauce-labs-backpack")
    inventario.agregar_producto("sauce-labs-bike-light")
    assert inventario.cantidad_en_carrito() == 2

    inventario.abrir_carrito()
    carrito = CartPage(driver)
    assert carrito.cantidad_articulos() == 2

    carrito.pagar("Mauricio", "QA", "55000")
    assert carrito.subtotal() == 39.98
    assert carrito.finalizar() == "Thank you for your order!"
