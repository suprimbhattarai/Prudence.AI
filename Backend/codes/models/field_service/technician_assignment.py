from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class TechnicianAssignment(Base):
    __tablename__ = "technician_assignments"

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

    technician_id: Mapped[int] = mapped_column(
        ForeignKey(
            "technician_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="assigned",
        nullable=False,
        index=True,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    appointment = relationship(
        "Appointment",
        back_populates="assignments",
    )

    technician = relationship(
        "TechnicianProfile",
        back_populates="assignments",
    )

    visits = relationship(
        "ServiceVisit",
        back_populates="technician_assignment",
        cascade="all, delete-orphan",
    )
