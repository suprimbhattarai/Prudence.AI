from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from codes.database import get_db

from codes.dependencies.authentication import get_current_admin
from codes.models.users.user import User

from codes.schemas.admin.technician_verification import (
    PendingTechnicianResponse,
    TechnicianVerificationResponse,
)
from codes.services.admin.technician_verification_service import (
    TechnicianVerificationService,
)

router = APIRouter(
    prefix="/api/v1/admin/technicians",
    tags=["Admin - Technician Verification"],
)


@router.get(
    "/pending",
    response_model=list[PendingTechnicianResponse],
)
def get_pending_technicians(
    admin: Annotated[User, Depends(get_current_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    return TechnicianVerificationService(db).get_pending_technicians(admin)


@router.patch(
    "/{technician_id}/verify",
    response_model=TechnicianVerificationResponse,
)
def verify_technician(
    technician_id: int,
    admin: Annotated[User, Depends(get_current_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    return TechnicianVerificationService(db).verify_technician(
        technician_id=technician_id,
        admin=admin,
    )
