import requests
from bs4 import BeautifulSoup

from backend.security.url_validator import validate_url


def fetch_webpage(url: str) -> str:
    current_url = url
    max_redirects = 3

    for _ in range(max_redirects + 1):
        validate_url(current_url)

        response = requests.get(
            current_url,
            timeout=(5, 10),
            headers={
                "User-Agent": "AutoSecurePipeline/1.0"
            },
            allow_redirects=False,
        )

        if response.is_redirect:
            next_url = response.headers.get("Location")

            if not next_url:
                raise ValueError("Redirect response has no Location header.")

            current_url = next_url
            continue

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type", ""
        ).lower()

        if "text/html" not in content_type:
            raise ValueError("URL did not return an HTML document.")

        max_size = 5 * 1024 * 1024

        content_length = response.headers.get("Content-Length")

        if content_length and int(content_length) > max_size:
            raise ValueError("Response is too large.")

        if len(response.content) > max_size:
            raise ValueError("Response is too large.")

        return response.text

    raise ValueError("Too many redirects.")


def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for element in soup(["script", "style", "noscript"]):
        element.decompose()

    return soup.get_text(separator=" ", strip=True)