import pytest
from backend.services.scraper_service import fetch_webpage
from backend.security.url_validator import (
    UnsafeURLError,
    validate_url,
)


def test_https_url_is_allowed():
    validate_url("https://example.com")


def test_http_url_is_allowed():
    validate_url("http://example.com")


def test_ftp_is_blocked():
    with pytest.raises(UnsafeURLError):
        validate_url("ftp://example.com")


def test_localhost_is_blocked():
    with pytest.raises(UnsafeURLError):
        validate_url("http://localhost")


def test_loopback_ip_is_blocked():
    with pytest.raises(UnsafeURLError):
        validate_url("http://127.0.0.1")


def test_scraper_blocks_localhost():
    with pytest.raises(UnsafeURLError):
        fetch_webpage("http://localhost")


def test_scraper_blocks_loopback_ip():
    with pytest.raises(UnsafeURLError):
        fetch_webpage("http://127.0.0.1")