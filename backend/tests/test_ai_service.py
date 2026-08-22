from backend.services.ai_service import analyze_text


VALID_CATEGORIES = {
    "retail",
    "technology",
    "finance",
    "travel",
    "food",
    "automotive",
    "healthcare",
    "education",
    "general",
}


VALID_CONTENT_TYPES = {
    "tutorial",
    "article",
    "documentation",
    "product",
    "dataset",
    "business",
    "informational",
    "other",
}


def test_ai_analysis_returns_result():
    result = analyze_text(
        "This is a product description for a laptop."
    )

    assert result.summary
    assert result.category in VALID_CATEGORIES
    assert 0.0 <= result.confidence <= 1.0
    assert isinstance(result.keywords, list)
    assert result.content_type in VALID_CONTENT_TYPES


def test_ai_classifies_technology_content():
    result = analyze_text(
        """
        Python is a programming language used for software development,
        automation, machine learning, data science and web applications.
        """
    )

    assert result.category == "technology"
    assert result.confidence > 0.5
    assert result.summary
    assert result.keywords