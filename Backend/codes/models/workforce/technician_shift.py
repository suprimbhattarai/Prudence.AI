from datetime import time

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, SmallInteger, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class TechnicianShift(Base):
    __tablename__ = "technician_shifts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    technician_id: Mapped[int] = mapped_column(
        ForeignKey(
            "technician_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    day_of_week: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    technician = relationship(
        "TechnicianProfile",
        back_populates="shifts",
    )

    __table_args__ = (
        CheckConstraint(
            "day_of_week BETWEEN 0 AND 6",
            name="ck_technician_shift_day_of_week",
        ),
        CheckConstraint(
            "start_time < end_time",
            name="ck_technician_shift_time_range",
        ),
    )
