from playwright.sync_api import Page


class Header:
    def __init__(self, page: Page):
        self.page = page
        self.user_menu = page.get_by_test_id("nav-menu")