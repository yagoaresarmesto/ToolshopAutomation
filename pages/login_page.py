from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.email_input = page.get_by_test_id("email")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-submit")

        self.email_error_message = page.get_by_test_id("email-error")
        self.password_error_message = page.get_by_test_id("password-error")
        self.login_error_message = page.get_by_test_id("login-error")

        self.register_link = page.get_by_test_id("register-link")


    def open(self):
        self.page.goto("/auth/login")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def go_to_register(self):
        self.register_link.click()