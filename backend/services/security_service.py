from dataclasses import dataclass
import re


@dataclass
class SecurityResult:
    is_safe: bool
    issues: list[str]


SUSPICIOUS_PATTERNS = [
    r"<script\b",
    r"javascript:",
    r"DROP\s+TABLE",
    r"UNION\s+SELECT",
    r"<iframe\b",
]


def analyze_content(text: str) -> SecurityResult:
    issues = []

    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            issues.append(
                f"Suspicious pattern detected: {pattern}"
            )

    return SecurityResult(
        is_safe=len(issues) == 0,
        issues=issues,
    )