from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from codes.models.base import Base


class CustomerDevice(Base):
    __tablename__ = "customer_devices"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    service_id: Mapped[int] = mapped_column(
        ForeignKey(
            "customer_services.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    device_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    model: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    serial_number: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        index=True,
    )

    mac_address: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    service = relationship(
        "CustomerService",
        back_populates="devices",
    )
