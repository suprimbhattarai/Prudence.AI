from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base


class TeamServiceZone(Base):
    __tablename__ = "team_service_zones"

    team_id: Mapped[int] = mapped_column(
        ForeignKey(
            "teams.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    service_zone_id: Mapped[int] = mapped_column(
        ForeignKey(
            "service_zones.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    team = relationship(
        "Team",
        back_populates="service_zones",
    )

    service_zone = relationship(
        "ServiceZone",
        back_populates="teams",
    )
