from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from codes.database import get_db
from codes.schemas.organizations.organization_response import (
    OrganizationResponse,
)
from codes.services.organizations.organization_service import (
    OrganizationService,
)

router = APIRouter(
    prefix="/api/v1/organizations",
    tags=["Organizations"],
)


@router.get(
    "/available",
    response_model=list[OrganizationResponse],
)
def get_available_organizations(
    db: Annotated[Session, Depends(get_db)],
):
    return OrganizationService(db).get_available_organizations()
