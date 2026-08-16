from backend.security.url_validator import (
    UnsafeURLError,
    validate_url,
)


safe_urls = [
    "https://example.com",
    "https://www.python.org",
]


unsafe_urls = [
    "http://127.0.0.1",
    "http://localhost",
    "ftp://example.com",
]


for url in safe_urls:
    validate_url(url)
    print("ALLOWED:", url)


for url in unsafe_urls:
    try:
        validate_url(url)
        print("ERROR - SHOULD HAVE BEEN BLOCKED:", url)
    except UnsafeURLError as exc:
        print("BLOCKED:", url)
        print("Reason:", exc)