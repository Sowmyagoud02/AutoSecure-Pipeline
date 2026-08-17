from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.models.ingestion import Ingestion, ProcessingStatus
from backend.models.user import User
from backend.schemas.ingestion import URLIngestionRequest
from backend.security.dependencies import get_current_user
from backend.security.url_validator import UnsafeURLError, validate_url
from backend.services.scraper_service import fetch_webpage, extract_text
from backend.services.validation_service import validate_text
from backend.services.security_service import analyze_content


router = APIRouter(
    prefix="/ingest",
    tags=["Ingestion"],
)


@router.post(
    "/url",
    status_code=status.HTTP_201_CREATED,
)
def ingest_url(
    data: URLIngestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        validate_url(str(data.url))

    except UnsafeURLError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    ingestion = Ingestion(
        source_type="url",
        original_name=str(data.url),
        source_url=str(data.url),
        processing_status=ProcessingStatus.PENDING,
        user_id=current_user.id,
    )

    db.add(ingestion)
    db.commit()
    db.refresh(ingestion)

    try:
        html = fetch_webpage(str(data.url))
        text = extract_text(html)

        validation_result = validate_text(text)

        if not validation_result.is_valid:
            ingestion.validation_status = "failed"
            ingestion.processing_status = ProcessingStatus.FAILED

            db.commit()

            return {
                "id": ingestion.id,
                "source_url": ingestion.source_url,
                "status": "failed",
                "validation_status": "failed",
                "issues": validation_result.issues,
            }

        security_result = analyze_content(text)

        if not security_result.is_safe:
            ingestion.security_status = "failed"
            ingestion.processing_status = ProcessingStatus.FAILED

            db.commit()

            return {
                "id": ingestion.id,
                "source_url": ingestion.source_url,
                "status": "failed",
                "validation_status": "passed",
                "security_status": "failed",
                "security_issues": security_result.issues,
            }

        ingestion.validation_status = "passed"
        ingestion.security_status = "passed"
        ingestion.processing_status = ProcessingStatus.COMPLETED

        db.commit()
        db.refresh(ingestion)

        return {
            "id": ingestion.id,
            "source_url": ingestion.source_url,
            "status": "completed",
            "validation_status": "passed",
            "security_status": "passed",
            "text_length": validation_result.text_length,
            "text_preview": text[:500],
        }

    except Exception as exc:
        ingestion.processing_status = ProcessingStatus.FAILED

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to fetch webpage: {str(exc)}",
        )