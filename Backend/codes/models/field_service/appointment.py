from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tickets.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey(
            "customer_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    service_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "customer_services.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    scheduled_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    scheduled_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="scheduled",
        nullable=False,
        index=True,
    )

    customer_note: Mapped[str | None] = mapped_column(
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

    ticket = relationship(
        "Ticket",
        back_populates="appointments",
    )

    customer = relationship(
        "CustomerProfile",
        back_populates="appointments",
    )

    service = relationship(
        "CustomerService",
        back_populates="appointments",
    )

    assignments = relationship(
        "TechnicianAssignment",
        back_populates="appointment",
        cascade="all, delete-orphan",
        order_by="TechnicianAssignment.assigned_at",
    )

    visits = relationship(
        "ServiceVisit",
        back_populates="appointment",
        cascade="all, delete-orphan",
    )
