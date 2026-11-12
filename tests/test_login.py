import pytest
from playwright.sync_api import Page, expect
from components.header import Header
from pages.login_page import LoginPage
from pages.account_page import AccountPage


# Jira: TSA-5 — Successful sign-in with valid customer credentials
def test_customer_can_login_with_valid_credentials(page: Page, customer):
    login_page = LoginPage(page)
    account_page = AccountPage(page)
    header = Header(page)

    login_page.open()
    login_page.login(customer["email"], customer["password"])

    expect(account_page.heading).to_be_visible()
    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/account"
    )
    expect(header.user_menu).to_have_text(customer["name"])

# Jira: TSA-6 — Sign-in with an incorrect password
@pytest.mark.usefixtures("customer_with_reset_login_attempts")
def test_customer_cannot_login_with_incorrect_password(page: Page, customer):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login(customer["email"], "WrongPassword123!")

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

# Jira: TSA-11 — Sign-in with an invalid email format
@pytest.mark.parametrize(
    "invalid_email",
    [
        "customer.example.com",
        "@example.com",
        "customer@",
        "cus tomer@example.com",
    ],
)

def test_customer_cannot_login_with_invalid_email_format(page: Page, invalid_email: str):
    login_page = LoginPage(page)

    login_page.open()

    login_page.login(invalid_email, "welcome01")

    expect(login_page.email_error_message).to_be_visible()

    expect(login_page.password_error_message).not_to_be_visible()

    expect(login_page.email_error_message).to_have_text(
        "Email format is invalid"
    )

    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/auth/login"
    )

# Jira: TSA-12 — Successful sign-in after correcting an incorrect password
@pytest.mark.usefixtures("customer_with_reset_login_attempts")
def test_customer_can_login_after_correcting_password(page: Page, customer):
    login_page = LoginPage(page)
    account_page = AccountPage(page)
    header = Header(page)

    login_page.open()

    login_page.login(customer["email"], "SoftwaretestingQA#02")

    expect(login_page.email_error_message).not_to_be_visible()

    expect(login_page.login_error_message).to_be_visible()
    expect(login_page.login_error_message).to_have_text(
        "Invalid email or password"
    )

    login_page.login(customer["email"], customer["password"])
    expect(account_page.heading).to_be_visible()
    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/account"
    )
    expect(header.user_menu).to_have_text(customer["name"])

# Jira: TSA-13 — Successful sign-in after completing required fields
def test_customer_can_login_after_completing_required_fields(page: Page, customer):
    login_page = LoginPage(page)
    account_page = AccountPage(page)
    header = Header(page)

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

    login_page.login(customer["email"], customer["password"])
    expect(account_page.heading).to_be_visible()
    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/account"
    )
    expect(header.user_menu).to_have_text(customer["name"])

# Jira: TSA-14 — Successful sign-in after correcting an invalid email format
def test_customer_can_login_after_correcting_email_format(page: Page, customer):
    login_page = LoginPage(page)
    account_page = AccountPage(page)
    header = Header(page)

    login_page.open()

    login_page.login("customer.example.com", customer["password"])

    expect(login_page.email_error_message).to_be_visible()

    expect(login_page.password_error_message).not_to_be_visible()

    expect(login_page.email_error_message).to_have_text(
        "Email format is invalid"
    )

    login_page.login(customer["email"], customer["password"])
    expect(account_page.heading).to_be_visible()
    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/account"
    )
    expect(header.user_menu).to_have_text(customer["name"])


# Jira: TSA-15 — Password is masked by default
def test_password_is_masked_by_default(page: Page):
    login_page = LoginPage(page)

    login_page.open()

    expect(login_page.password_input).to_have_attribute("type", "password")

    login_page.password_input.fill("MaskCheck123!")

    expect(login_page.password_input).to_have_attribute("type", "password")

# Jira: TSA-16 — Navigate from sign-in to customer registration
def test_visitor_can_navigate_to_registration(page: Page):
    login_page = LoginPage(page)

    login_page.open()

    login_page.go_to_register()

    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/auth/register"
    )

    expect(
        page.get_by_role(
            "heading", name="Customer registration", exact=True
        )
    ).to_be_visible()

# Jira: TSA-17 — Navigate from sign-in to password recovery
def test_visitor_can_navigate_to_password_recovery(page: Page):
    login_page = LoginPage(page)

    login_page.open()

    login_page.go_to_forgot_password()

    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/auth/forgot-password"
    )

    expect(
        page.get_by_role(
            "heading", name="Forgot Password", exact=True
        )
    ).to_be_visible()

# Jira: TSA-18 — Show and hide the password using the visibility toggle
def test_visitor_can_toggle_password_visibility(page: Page):
    login_page = LoginPage(page)

    login_page.open()

    login_page.password_input.fill("MaskCheck123!")

    expect(login_page.password_input).to_have_attribute("type", "password")

    login_page.toggle_password_visibility()

    expect(login_page.password_input).to_have_attribute("type", "text")

    login_page.toggle_password_visibility()

    expect(login_page.password_input).to_have_attribute("type", "password")