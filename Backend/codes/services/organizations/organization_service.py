from sqlalchemy.orm import Session

from codes.repositories.organizations.organization_repository import (
    OrganizationRepository,
)


class OrganizationService:
    def __init__(self, db: Session):
        self.repository = OrganizationRepository(db)

    def get_available_organizations(self):
        return self.repository.get_active_organizations()
