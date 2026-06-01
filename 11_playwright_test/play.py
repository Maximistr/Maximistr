from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://store.supercell.com/brawlstars")
    time.sleep(2)

    page.get_by_role("button", name="Accept All Cookies").click()
    time.sleep(2)
    buttons = page.get_by_role("button").all()

    for button in buttons:

     print(button.text_content())

    time.sleep(5)