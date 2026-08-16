import ipaddress
import socket
from urllib.parse import urlparse


class UnsafeURLError(ValueError):
    """Raised when a URL is considered unsafe to access."""


def validate_url(url: str) -> None:
    parsed = urlparse(url)

    # Only allow HTTP and HTTPS.
    if parsed.scheme not in {"http", "https"}:
        raise UnsafeURLError("Only HTTP and HTTPS URLs are allowed.")

    # A hostname is required.
    if not parsed.hostname:
        raise UnsafeURLError("URL must contain a hostname.")

    hostname = parsed.hostname

    # Resolve the hostname to an IP address.
    try:
        ip_addresses = socket.getaddrinfo(
            hostname,
            None,
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror as exc:
        raise UnsafeURLError("Unable to resolve hostname.") from exc

    for address in ip_addresses:
        ip = ipaddress.ip_address(address[4][0])

        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
        ):
            raise UnsafeURLError(
                "Access to private or reserved IP addresses is not allowed."
            )