import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configura los contextos de pruebas con idioma inglés."""
    return {
        **browser_context_args,
        "locale": "en-US",
    }