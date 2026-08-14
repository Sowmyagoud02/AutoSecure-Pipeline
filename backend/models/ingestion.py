from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base


class SourceType(str, Enum):
    FILE = "file"
    URL = "url"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class CheckStatus(str, Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"


class Ingestion(Base):
    __tablename__ = "ingestions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    source_type: Mapped[SourceType] = mapped_column(
        String(20),
        nullable=False,
    )

    original_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    stored_filename: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )

    file_type: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    file_size: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    processing_status: Mapped[ProcessingStatus] = mapped_column(
        String(20),
        default=ProcessingStatus.PENDING,
        nullable=False,
    )

    validation_status: Mapped[CheckStatus] = mapped_column(
        String(20),
        default=CheckStatus.PENDING,
        nullable=False,
    )

    security_status: Mapped[CheckStatus] = mapped_column(
        String(20),
        default=CheckStatus.PENDING,
        nullable=False,
    )

    ai_status: Mapped[CheckStatus] = mapped_column(
        String(20),
        default=CheckStatus.PENDING,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="ingestions",
    )