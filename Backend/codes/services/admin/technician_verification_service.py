from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from codes.core.enums.user_role import UserRole
from codes.models.users.user import User

from codes.repositories.auth.user_repository import UserRepository


class TechnicianVerificationService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def get_pending_technicians(
        self,
        admin: User,
    ) -> list[dict]:
        self._require_admin(admin)

        records = self.users.get_pending_technicians(
            organization_id=admin.organization_id
        )

        return [
            {
                "id": user.id,
                "email": user.email,
                "full_name": profile.full_name,
                "employee_code": profile.employee_code,
                "organization_id": user.organization_id,
            }
            for user, profile in records
        ]

    def verify_technician(
        self,
        *,
        technician_id: int,
        admin: User,
    ) -> User:
        self._require_admin(admin)

        try:
            technician = self.users.get_technician_for_update(
                user_id=technician_id,
                organization_id=admin.organization_id,
            )

            if technician is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Technician not found",
                )

            if technician.is_verified:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Technician is already verified",
                )

            technician.is_verified = True

            self.db.commit()
            self.db.refresh(technician)

            return technician

        except Exception:
            self.db.rollback()
            raise

    @staticmethod
    def _require_admin(admin: User) -> None:
        if admin.role != UserRole.ADMIN or not admin.is_active or not admin.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Administrator permission required",
            )
