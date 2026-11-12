import pytest
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