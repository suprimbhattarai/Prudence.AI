from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    ticket_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
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

    complaint_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "complaints.id",
            ondelete="SET NULL",
        ),
        unique=True,
        nullable=True,
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

    status: Mapped[str] = mapped_column(
        String(30),
        default="open",
        nullable=False,
        index=True,
    )

    priority: Mapped[str] = mapped_column(
        String(30),
        default="normal",
        nullable=False,
        index=True,
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

    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    customer = relationship(
        "CustomerProfile",
        back_populates="tickets",
    )

    complaint = relationship(
        "Complaint",
        back_populates="ticket",
    )

    service = relationship(
        "CustomerService",
        back_populates="tickets",
    )

    events = relationship(
        "TicketEvent",
        back_populates="ticket",
        cascade="all, delete-orphan",
        order_by="TicketEvent.created_at",
    )

    appointments = relationship(
        "Appointment",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )

    feedback_entries = relationship(
        "Feedback",
        back_populates="ticket",
    )
