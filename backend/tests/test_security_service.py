from backend.services.security_service import analyze_content


def test_normal_content_is_safe():
    result = analyze_content(
        "This is a normal product description with a price of 99 euros."
    )

    assert result.is_safe is True
    assert result.issues == []


def test_script_is_detected():
    result = analyze_content(
        '<script>alert("test")</script>'
    )

    assert result.is_safe is False
    assert len(result.issues) > 0


def test_javascript_is_detected():
    result = analyze_content(
        'javascript:alert("test")'
    )

    assert result.is_safe is False


def test_sql_pattern_is_detected():
    result = analyze_content(
        "UNION SELECT username, password FROM users"
    )

    assert result.is_safe is False