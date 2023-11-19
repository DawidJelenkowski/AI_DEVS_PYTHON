import json
import re
from markdownify import markdownify as md
from playwright.sync_api import sync_playwright


def scrape_web_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='domcontentloaded')
        content = page.query_selector('.main').inner_html()
        browser.close()
        return content


def replace_url_with_placeholder(match):
    url = match.group(0)
    if url not in url_to_placeholder:
        placeholder = f"${placeholder_count[0]}"
        url_to_placeholder[url] = placeholder
        placeholder_count[0] += 1
    return url_to_placeholder[url]


# URL to scrape
url = "https://brain.overment.com"

# Scrape the webpage and get HTML content
html_content = scrape_web_page(url)

# Convert HTML to Markdown
markdown_content = md(html_content)

# Process the markdown content to replace URLs with placeholders
url_to_placeholder = {}
placeholder_count = [1]

processed_markdown = re.sub(
    r"((http|https)://[^\s]+|\./[^\s]+)(?=\))", replace_url_with_placeholder, markdown_content)

# Save the results to a file
docs = {
    'pageContent': processed_markdown,
    'metadata': url_to_placeholder
}

with open("lanchain_python/12_web/output.json", "w") as file:
    json.dump(docs, file, indent=2)
