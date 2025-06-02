from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import random

from bs4 import BeautifulSoup
import markdownify
import re


def scrape(URL: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )
        
        context = browser.new_context(
            
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            viewport={"width": 1920, "height": 1080}
            # proxy={'server': '188.127.231.160:49160'}
        )

        stealth_sync(context)
        
        page = context.new_page()

        page.route("**/*", lambda route: route.abort() if "adservice" in route.request.url else route.continue_())

        page.evaluate('''() => {
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
        }''')

        try:
            page.wait_for_timeout(random.uniform(2, 5) * 1000)
            page.goto(URL)

            html_page = page.content()

            page.wait_for_timeout(random.uniform(2, 5) * 1000)
        except Exception as e:
            print('Error: ', e)
        finally:
            browser.close()

        return html_page


def split_content(dom_content: str, max_length: int=6000) -> list:
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


def cleaning_html_page(html_page: str) -> str:
    soup = BeautifulSoup(html_page, 'html.parser')
    for tag in soup(['script', 'style', 'nav', 'footer', 'aside']):
        tag.extract()

    markdown = markdownify.markdownify(str(soup), heading_style='atx')
    markdown = re.sub(r'\s+', ' ', markdown).strip()

    markdown = markdown.replace('"', "'")

    return markdown

