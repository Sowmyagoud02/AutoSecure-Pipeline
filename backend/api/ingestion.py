from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.database.dependencies import get_db
from backend.models.ingestion import Ingestion, ProcessingStatus
from backend.models.user import User
from backend.schemas.ingestion import URLIngestionRequest
from backend.security.dependencies import get_current_user


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

    return ingestion