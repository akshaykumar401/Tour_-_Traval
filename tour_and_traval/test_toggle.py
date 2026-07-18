from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///tmp/test_page.html")
    page.wait_for_selector('#tab-html')
    page.click('#tab-html')
    
    # Check if textarea is visible
    is_visible = page.is_visible('#id_message')
    print("Is Textarea Visible?", is_visible)
    browser.close()
