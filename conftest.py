import pytest
from playwright.sync_api import Playwright
from data.users import CUSTOMER


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configura los contextos de pruebas con idioma inglés."""
    return {
        **browser_context_args,
        "locale": "en-US",
    }

@pytest.fixture(scope="session", autouse=True)
def configure_test_id_attribute(playwright: Playwright):
    """Utiliza el atributo de pruebas definido por Toolshop."""
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture
def customer_with_reset_login_attempts(playwright: Playwright):
    """Reinicia los intentos fallidos antes y después del test."""
    api = playwright.request.new_context(
        base_url="https://api.practicesoftwaretesting.com"
    )

    def reset_login_attempts():
        response = api.post(
            "/users/login",
            data={
                "email": CUSTOMER["email"],
                "password": CUSTOMER["password"],
            },
        )

        assert response.status == 200, (
            "No se pudo reiniciar el contador mediante un login válido. "
            f"Estado HTTP: {response.status}"
        )

    try:
        reset_login_attempts()
        yield
    finally:
        try:
            reset_login_attempts()
        finally:
            api.dispose()