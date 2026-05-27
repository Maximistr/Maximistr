from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://store.supercell.com/brawlstars")
    time.sleep(2)

    # Use 'button:visible' to get only the buttons a user can see
    # .all() converts the locator group into a Python list of individual elements
    page.get_by_role("button", name="Accept All Cookies").click()

    time.sleep(10)