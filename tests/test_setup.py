from playwright.sync_api import Page, expect


def test_login_page_is_accessible(page: Page):
    page.goto("/auth/login")

    expect(page).to_have_url(
        "https://practicesoftwaretesting.com/auth/login"
    )
    expect(
        page.get_by_role("heading", name="Login", exact=True)
    ).to_be_visible()