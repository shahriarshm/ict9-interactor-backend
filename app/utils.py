from bs4 import BeautifulSoup
from app.config import settings


def add_default_js_to_html(html_string: str) -> str:
    """
    Adds the default JS URL as a script tag in the HTML head.

    Args:
        html_string (str): The original HTML string.

    Returns:
        str: The modified HTML string with the default JS script tag added.
    """
    soup = BeautifulSoup(html_string, "html.parser")

    script_tag = soup.new_tag("script", src=settings.DEFAULT_JS_URL)

    if not soup.head:
        head = soup.new_tag("head")
        soup.html.insert(0, head)

    soup.head.append(script_tag)

    return str(soup)
