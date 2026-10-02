from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, SmallInteger, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "customer_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    ticket_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "tickets.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    service_visit_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "service_visits.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    rating: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    customer = relationship(
        "CustomerProfile",
        back_populates="feedback_entries",
    )

    ticket = relationship(
        "Ticket",
        back_populates="feedback_entries",
    )

    service_visit = relationship(
        "ServiceVisit",
        back_populates="feedback_entries",
    )

    __table_args__ = (
        CheckConstraint(
            "rating BETWEEN 1 AND 5",
            name="ck_feedback_rating",
        ),
    )
