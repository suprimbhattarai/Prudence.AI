from sqlalchemy import CheckConstraint, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base


class TechnicianSkill(Base):
    __tablename__ = "technician_skills"

    technician_id: Mapped[int] = mapped_column(
        ForeignKey(
            "technician_profiles.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey(
            "skills.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    proficiency_level: Mapped[int] = mapped_column(
        SmallInteger,
        default=1,
        nullable=False,
    )

    technician = relationship(
        "TechnicianProfile",
        back_populates="technician_skills",
    )

    skill = relationship(
        "Skill",
        back_populates="technician_skills",
    )

    __table_args__ = (
        CheckConstraint(
            "proficiency_level BETWEEN 1 AND 5",
            name="ck_technician_skill_proficiency",
        ),
    )
