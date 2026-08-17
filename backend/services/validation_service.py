from dataclasses import dataclass


@dataclass
class ValidationResult:
    is_valid: bool
    text_length: int
    issues: list[str]


def validate_text(text: str) -> ValidationResult:
    issues = []

    if not text.strip():
        issues.append("Extracted text is empty.")

    if len(text) < 20:
        issues.append("Extracted text is too short.")

    return ValidationResult(
        is_valid=len(issues) == 0,
        text_length=len(text),
        issues=issues,
    )