from playwright.sync_api import Page

class AccountPage:
    def __init__(self, page: Page):
        self.page = page

        self.heading = page.get_by_role(
            "heading", name="My account", exact=True
        )

