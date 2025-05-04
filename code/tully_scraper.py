import re
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.tullysgoodtimes.com/menus/")

    all_menu_items = []

    # Menu section titles
    titles = page.locator(".menu-section-title")
    title_count = titles.count()

    for i in range(title_count):
        title_element = titles.nth(i)
        title_text = title_element.inner_text().strip()

        # The actual menu items are a couple divs down — fix selector here
        # Look for the first `.row` div *after* the title
        section_div = title_element.locator("xpath=ancestor::div[contains(@class, 'menu-section')]/following-sibling::div[contains(@class, 'row')]").first

        if not section_div:
            print(f"Could not find section div for title: {title_text}")
            continue

        # Individual item blocks
        item_elements = section_div.locator(".col-md-12")

        for j in range(item_elements.count()):
            item_block = item_elements.nth(j)
            item_text = item_block.inner_text().strip()

            if item_text:
                try:
                    menu_item = extract_menu_item(title_text, item_text)
                    all_menu_items.append(menu_item.to_dict())
                except Exception as e:
                    print(f"Error extracting item under '{title_text}': {e}\nText:\n{item_text}\n")

    # Write to CSV
    if all_menu_items:
        df = pd.DataFrame(all_menu_items)
        df.to_csv("cache/tullys_menu.csv", index=False)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    tullyscraper(playwright)