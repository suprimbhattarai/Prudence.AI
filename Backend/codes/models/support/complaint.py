from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class Complaint(Base):
    __tablename__ = "complaints"

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

    conversation_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "conversations.id",
            ondelete="SET NULL",
        ),
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

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    priority: Mapped[str] = mapped_column(
        String(30),
        default="normal",
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="open",
        nullable=False,
        index=True,
    )

    reported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    customer = relationship(
        "CustomerProfile",
        back_populates="complaints",
    )

    conversation = relationship(
        "Conversation",
        back_populates="complaints",
    )

    service = relationship(
        "CustomerService",
        back_populates="complaints",
    )

    complaints = relationship(
        "Complaint",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    ticket = relationship(
        "Ticket",
        back_populates="complaint",
        uselist=False,
    )
