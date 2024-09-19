from bs4 import BeautifulSoup
from app.config import settings
import openai

client = openai.OpenAI(
    base_url=settings.OPENAI_API_URL, api_key=settings.OPENAI_API_KEY
)


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


def is_html_safe(html_content: str) -> bool:
    """
    Checks if the given HTML content is safe using GPT-4o-mini.

    This function sends the HTML content to the GPT-4o-mini model to analyze for potential security risks such as:
    - Sensitive content (e.g., personal information, explicit content)
    - Malicious script tags
    - Iframe injections
    - Potentially harmful attributes (e.g., onload, onerror)

    Args:
        html_content (str): The HTML content to be checked.

    Returns:
        str: "Yes" if the HTML is considered safe, "No" otherwise.
    """
    prompt = f"""
    Analyze the following HTML content for safety. Consider the following aspects:
    1. Presence of sensitive content (e.g., personal information, explicit content)
    2. Potentially malicious script tags
    3. Iframe injections
    4. Harmful attributes (e.g., onload, onerror)
    5. Any other security concerns

    Respond with only 'Yes' if the HTML is safe, or 'No' if it's not safe.

    HTML Content:
    {html_content}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a security expert analyzing HTML content."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1,
        )
        result = response.choices[0].message.content.strip().lower()
        return True if result == "yes" else False
    except Exception as e:
        print(f"Error in LLM analysis: {str(e)}")
        return False  # Default to unsafe if there's an error
