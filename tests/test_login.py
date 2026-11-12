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

# Jira: TSA-6 — Sign-in with an incorrect password
def test_customer_cannot_login_with_incorrect_password(page: Page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login("customer@practicesoftwaretesting.com", "WrongPassword123!")

    expect(login_page.login_error_message).to_be_visible()
    expect(login_page.login_error_message).to_have_text(
        "Invalid email or password"
    )

    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/auth/login"
    )

# Jira: TSA-7 — Sign-in with an unregistered email address
def test_customer_cannot_login_with_unregistered_email(page: Page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login("qa-login-unregistered-48291@example.com", "WrongPassword123!")

    expect(login_page.login_error_message).to_be_visible()
    expect(login_page.login_error_message).to_have_text(
        "Invalid email or password"
    )

    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/auth/login"
    )

# Jira: TSA-8 — Sign-in with both fields empty
def test_customer_cannot_login_with_empty_fields(page: Page):
    login_page = LoginPage(page)

    login_page.open()

    login_page.login("", "")
    expect(login_page.email_error_message).to_be_visible()
    expect(login_page.password_error_message).to_be_visible()

    expect(login_page.email_error_message).to_have_text(
        "Email is required"
    )
    expect(login_page.password_error_message).to_have_text(
        "Password is required"
    )

    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/auth/login"
    )

# Jira: TSA-9 — Sign-in with an empty email address
def test_customer_cannot_login_with_empty_email(page: Page):
    login_page = LoginPage(page)

    login_page.open()

    login_page.login("", "welcome01")
    expect(login_page.email_error_message).to_be_visible()

    expect(login_page.password_error_message).not_to_be_visible()

    expect(login_page.email_error_message).to_have_text(
        "Email is required"
    )

    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/auth/login"
    )

# Jira: TSA-10 — Sign-in with an empty password
def test_customer_cannot_login_with_empty_password(page: Page):
    login_page = LoginPage(page)

    login_page.open()

    login_page.login("customer@practicesoftwaretesting.com", "")
    expect(login_page.email_error_message).not_to_be_visible()

    expect(login_page.password_error_message).to_be_visible()

    expect(login_page.password_error_message).to_have_text(
        "Password is required"
    )

    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/auth/login"
    )