from playwright.sync_api import Page, expect

from components.header import Header
from pages.login_page import LoginPage
from pages.account_page import AccountPage


# Jira: TSA-5 — Successful sign-in with valid customer credentials
# https://automationplaywright.atlassian.net/browse/TSA-5
def test_customer_can_login_with_valid_credentials(page: Page):
    login_page = LoginPage(page)
    account_page = AccountPage(page)
    header = Header(page)

    login_page.open()
    login_page.login("customer@practicesoftwaretesting.com", "welcome01")
    expect(account_page.heading).to_be_visible()
    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/account"
    )
    expect(header.user_menu).to_have_text("Jane Doe")