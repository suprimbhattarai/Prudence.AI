from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class ServiceReport(Base):
    __tablename__ = "service_reports"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    service_visit_id: Mapped[int] = mapped_column(
        ForeignKey(
            "service_visits.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    root_cause: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    work_performed: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    resolution: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    outcome: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    parts_used: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    service_visit = relationship(
        "ServiceVisit",
        back_populates="report",
    )
