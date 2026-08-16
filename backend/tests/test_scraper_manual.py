from backend.security.url_validator import UnsafeURLError
from backend.services.scraper_service import (
    fetch_webpage,
    extract_text,
)


safe_url = "https://example.com"

try:
    html = fetch_webpage(safe_url)

    print("HTML received:", len(html), "characters")

    text = extract_text(html)

    print("Extracted text:")
    print(text)

except Exception as exc:
    print("SAFE URL FAILED:", exc)


unsafe_url = "http://127.0.0.1"

try:
    fetch_webpage(unsafe_url)

    print("ERROR - UNSAFE URL WAS NOT BLOCKED")

except UnsafeURLError as exc:
    print("UNSAFE URL BLOCKED:", exc)