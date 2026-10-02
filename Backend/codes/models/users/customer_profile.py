from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class CustomerProfile(Base):
    __tablename__ = "customer_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="customer_profile",
    )

    addresses = relationship(
        "CustomerAddress",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    services = relationship(
        "CustomerService",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    conversations = relationship(
        "Conversation",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    tickets = relationship(
        "Ticket",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    appointments = relationship(
        "Appointment",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    feedback_entries = relationship(
        "Feedback",
        back_populates="customer",
        cascade="all, delete-orphan",
    )
