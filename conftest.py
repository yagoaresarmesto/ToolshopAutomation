import pytest
import os
from uuid import uuid4
from playwright.sync_api import Playwright


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
def customer_with_reset_login_attempts(
    playwright: Playwright, customer, api_base_url
):
    """Reinicia los intentos fallidos antes y después del test."""
    api = playwright.request.new_context(
        base_url=api_base_url
    )

    def reset_login_attempts():
        response = api.post(
            "/users/login",
            data={
                "email": customer["email"],
                "password": customer["password"],
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

@pytest.fixture(scope="session")
def customer(playwright: Playwright, api_base_url):
    """Crea un cliente exclusivo para la ejecución de pruebas."""
    unique_id = uuid4().hex

    registration_data = {
        "first_name": "Yago",
        "last_name": "Tester",
        "dob": "1990-01-15",
        "address": {
            "street": "Calle de Pruebas",
            "city": "Madrid",
            "state": "Madrid",
            "country": "ES",
            "postal_code": "28001",
        },
        "phone": "000000000",
        "email": f"toolshop-qa-{unique_id}@example.com",
        "password": "SoftwaretestingQA#01",
    }

    api = playwright.request.new_context(
        base_url=api_base_url
    )

    try:
        response = api.post(
            "/users/register",
            data=registration_data,
        )

        assert response.status == 201, (
            "No se pudo crear el cliente de pruebas. "
            f"Estado HTTP: {response.status}"
        )

        return {
            "email": registration_data["email"],
            "password": registration_data["password"],
            "name": (
                f"{registration_data['first_name']} "
                f"{registration_data['last_name']}"
            ),
        }
    finally:
        api.dispose()

@pytest.fixture(scope="session")
def api_base_url():
    """Permite configurar la API del entorno de pruebas."""
    return os.getenv(
        "TOOLSHOP_API_URL",
        "https://api.practicesoftwaretesting.com",
    )