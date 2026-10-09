from sqlalchemy import select
from sqlalchemy.orm import Session

from codes.models.organizations.organization import Organization


class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_active_organizations(self) -> list[Organization]:
        statement = (
            select(Organization)
            .where(Organization.is_active.is_(True))
            .order_by(Organization.name)
        )

        return list(self.db.scalars(statement).all())

    def get_active_by_id(
        self,
        organization_id: int,
    ) -> Organization | None:
        statement = select(Organization).where(
            Organization.id == organization_id,
            Organization.is_active.is_(True),
        )

        return self.db.scalar(statement)
