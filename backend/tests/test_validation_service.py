from backend.services.validation_service import validate_text


def test_valid_text():
    result = validate_text(
        "This is a valid webpage containing enough text."
    )

    assert result.is_valid is True
    assert result.text_length > 20
    assert result.issues == []


def test_empty_text():
    result = validate_text("")

    assert result.is_valid is False
    assert "Extracted text is empty." in result.issues


def test_short_text():
    result = validate_text("Hello")

    assert result.is_valid is False
    assert "Extracted text is too short." in result.issues