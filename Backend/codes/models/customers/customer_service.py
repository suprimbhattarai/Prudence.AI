from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class CustomerService(Base):
    __tablename__ = "customer_services"

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

    service_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    service_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    plan_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        nullable=False,
        index=True,
    )

    installation_address_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "customer_addresses.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    customer = relationship(
        "CustomerProfile",
        back_populates="services",
    )

    installation_address = relationship(
        "CustomerAddress",
    )

    devices = relationship(
        "CustomerDevice",
        back_populates="service",
        cascade="all, delete-orphan",
    )

    complaints = relationship(
        "Complaint",
        back_populates="service",
    )

    tickets = relationship(
        "Ticket",
        back_populates="service",
    )

    appointments = relationship(
        "Appointment",
        back_populates="service",
    )
