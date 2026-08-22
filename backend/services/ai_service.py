import json
import os
import re
from dataclasses import dataclass

import httpx


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b",
)


VALID_CATEGORIES = {
    "technology",
    "retail",
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


@dataclass
class AIAnalysisResult:
    summary: str
    category: str
    confidence: float
    keywords: list[str]
    content_type: str


def _extract_json(response_text: str) -> dict:
    """
    Extract JSON from the model response.

    Handles responses surrounded by markdown
    or additional text.
    """

    response_text = response_text.strip()

    response_text = re.sub(
        r"^```(?:json)?\s*",
        "",
        response_text,
        flags=re.IGNORECASE,
    )

    response_text = re.sub(
        r"\s*```$",
        "",
        response_text,
    )

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        match = re.search(
            r"\{.*\}",
            response_text,
            re.DOTALL,
        )

        if not match:
            raise ValueError(
                "AI model did not return valid JSON."
            )

        return json.loads(match.group(0))


def _normalize_category(category: str) -> str:
    """
    Ensure the model returns one of our supported categories.
    """

    category = str(category).strip().lower()

    if category in VALID_CATEGORIES:
        return category

    return "general"


def _normalize_content_type(content_type: str) -> str:
    """
    Ensure the model returns one of our supported content types.
    """

    content_type = str(content_type).strip().lower()

    if content_type in VALID_CONTENT_TYPES:
        return content_type

    return "other"


def _normalize_keywords(keywords) -> list[str]:
    """
    Normalize keyword output from the model.
    """

    if not isinstance(keywords, list):
        return []

    normalized = []

    for keyword in keywords:
        keyword = str(keyword).strip()

        if keyword and keyword not in normalized:
            normalized.append(keyword)

    return normalized[:10]


def analyze_text(text: str) -> AIAnalysisResult:
    """
    Analyze extracted and security-checked text
    using the local Ollama LLM.
    """

    if not text or not text.strip():
        raise ValueError(
            "Cannot analyze empty text."
        )

    # Limit input size for the local model.
    text_for_analysis = text[:12000]

    prompt = f"""
You are an AI content analysis engine inside a
secure automated data ingestion platform.

Your task is to understand the ACTUAL SUBJECT of the
provided content.

Return ONLY valid JSON.

Required structure:

{{
  "summary": "2-3 sentence meaningful summary of the actual content",
  "category": "technology | retail | finance | travel | food | automotive | healthcare | education | general",
  "confidence": 0.0,
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "content_type": "tutorial | article | documentation | product | dataset | business | informational | other"
}}

IMPORTANT CLASSIFICATION RULES:

- Focus on the main subject, not navigation menus,
  website branding, advertisements, footer text,
  login buttons, or unrelated links.

- technology:
  programming, software, APIs, databases, cloud,
  cybersecurity, development, AI, machine learning,
  programming languages, technical documentation.

- retail:
  shopping, stores, products, prices, customers,
  merchandising, supermarkets, e-commerce.

- finance:
  banking, investments, financial markets,
  accounting, insurance, economics and financial services.

- education:
  courses, teaching, learning resources,
  academic material and educational programs.

- healthcare:
  medicine, diseases, hospitals, treatments,
  healthcare services and medical research.

- The category must describe the PRIMARY subject.

SUMMARY RULES:

- Do not simply copy the beginning of the page.
- Do not summarize navigation menus.
- Explain what the content is actually about.
- Produce a useful summary that a human could understand
  without opening the original page.
- For tutorials, explain what the tutorial teaches.
- For products, explain what the product is and its purpose.
- For business pages, explain the organization/service.
- For articles, explain the main topic and key points.

CONFIDENCE RULES:

- Clearly identifiable subject: normally 0.80-0.98
- Moderately identifiable: 0.60-0.79
- Ambiguous content: below 0.60
- Never invent certainty.

KEYWORDS:

Return 3-10 meaningful keywords that represent
the actual subject.

CONTENT:

{text_for_analysis}
"""

    response = httpx.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        },
        timeout=120.0,
    )

    response.raise_for_status()

    data = response.json()

    model_response = data.get("response")

    if not model_response:
        raise ValueError(
            "Ollama returned an empty response."
        )

    result = _extract_json(model_response)

    summary = str(
        result.get("summary", "")
    ).strip()

    if not summary:
        raise ValueError(
            "AI model returned an empty summary."
        )

    category = _normalize_category(
        result.get("category", "general")
    )

    content_type = _normalize_content_type(
        result.get("content_type", "other")
    )

    try:
        confidence = float(
            result.get("confidence", 0.0)
        )
    except (TypeError, ValueError):
        confidence = 0.0

    confidence = max(
        0.0,
        min(confidence, 1.0),
    )

    keywords = _normalize_keywords(
        result.get("keywords", [])
    )

    return AIAnalysisResult(
        summary=summary,
        category=category,
        confidence=confidence,
        keywords=keywords,
        content_type=content_type,
    )