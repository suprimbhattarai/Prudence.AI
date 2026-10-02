from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class TechnicianAvailability(Base):
    __tablename__ = "technician_availability"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    technician_id: Mapped[int] = mapped_column(
        ForeignKey(
            "technician_profiles.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    is_on_duty: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    technician = relationship(
        "TechnicianProfile",
        back_populates="availability",
    )