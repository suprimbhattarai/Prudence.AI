from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class ServiceVisit(Base):
    __tablename__ = "service_visits"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    appointment_id: Mapped[int] = mapped_column(
        ForeignKey(
            "appointments.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    technician_assignment_id: Mapped[int] = mapped_column(
        ForeignKey(
            "technician_assignments.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="scheduled",
        nullable=False,
        index=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    technician_note: Mapped[str | None] = mapped_column(
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

    appointment = relationship(
        "Appointment",
        back_populates="visits",
    )

    technician_assignment = relationship(
        "TechnicianAssignment",
        back_populates="visits",
    )

    report = relationship(
        "ServiceReport",
        back_populates="service_visit",
        uselist=False,
        cascade="all, delete-orphan",
    )

    feedback_entries = relationship(
        "Feedback",
        back_populates="service_visit",
    )
