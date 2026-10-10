import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_login_valido(driver):
    LoginPage(driver).abrir().iniciar_sesion("standard_user", "secret_sauce")
    assert InventoryPage(driver).titulo() == "Products"


@pytest.mark.parametrize(
    "usuario, clave, mensaje",
    [
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out."),
        ("standard_user", "clave_mala", "Username and password do not match"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
)
def test_login_invalido(driver, usuario, clave, mensaje):
    login = LoginPage(driver).abrir()
    login.iniciar_sesion(usuario, clave)
    assert mensaje in login.texto_error()
