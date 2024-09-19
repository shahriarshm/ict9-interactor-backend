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


def is_html_safe(html_content: str) -> tuple[bool, str]:
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
        tuple[bool, str]: A tuple containing a boolean indicating if the HTML is safe,
                          and a string description of why it's not safe (empty if safe).
    """
    prompt = f"""
    Analyze the following HTML content for safety, considering it may contain Jinja templates. Consider the following aspects:
    1. Presence of sensitive content (e.g., personal information, explicit content)
    2. Potentially malicious script tags (excluding those that are part of Jinja templates)
    3. Iframe injections (excluding those that are part of Jinja templates)
    4. Harmful attributes (e.g., onload, onerror) (excluding those that are part of Jinja templates)
    5. Any other security concerns

    Note: Jinja template syntax should not be marked as unsafe.

    If the HTML is safe, respond with 'Yes'.
    If it's not safe, respond with 'No' followed by a brief description of the security concerns.

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
            max_tokens=100,
        )
        result = response.choices[0].message.content.strip()
        if result.lower().startswith("yes"):
            return True, ""
        else:
            return False, result[3:].strip()  # Remove 'No ' prefix and trim
    except Exception as e:
        print(f"Error in LLM analysis: {str(e)}")
        return False, "Error occurred during analysis"  # Default to unsafe if there's an error
