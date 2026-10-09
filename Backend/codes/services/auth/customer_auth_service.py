from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from codes.core.enums.user_role import UserRole
from codes.core.security.jwt import create_access_token
from codes.core.security.password import (
    hash_password,
    verify_password,
)

from codes.repositories.auth.user_repository import UserRepository
from codes.repositories.organizations.organization_repository import (
    OrganizationRepository,
)

from codes.schemas.auth.customer_login import UserLoginRequest
from codes.schemas.auth.customer_register import UserRegisterRequest


class CustomerAuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.organizations = OrganizationRepository(db)

    def register(self, data: UserRegisterRequest):
        organization = self.organizations.get_active_by_id(data.organization_id)

        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selected ISP is invalid or inactive",
            )

        existing_user = self.users.get_by_email(data.email)

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )

        if data.role == UserRole.TECHNICIAN:
            existing_technician = self.users.get_technician_by_employee_code(
                data.employee_code
            )

            if existing_technician is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Employee code is already registered",
                )

        verified = data.role == UserRole.CUSTOMER

        hashed_password = hash_password(data.password)

        try:
            user = self.users.create_user(
                email=data.email,
                hashed_password=hashed_password,
                role=data.role,
                organization_id=data.organization_id,
                is_verified=verified,
            )

            if data.role == UserRole.CUSTOMER:
                self.users.create_customer_profile(
                    user_id=user.id,
                    full_name=data.full_name,
                    phone=data.phone,
                )

            elif data.role == UserRole.TECHNICIAN:
                self.users.create_technician_profile(
                    user_id=user.id,
                    full_name=data.full_name,
                    phone=data.phone,
                    employee_code=data.employee_code,
                )

            self.db.commit()
            self.db.refresh(user)

            return user

        except IntegrityError:
            self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email or employee code already exists",
            )

        except Exception:
            self.db.rollback()
            raise

    def login(self, data: UserLoginRequest) -> str:
        user = self.users.get_by_email(data.email)

        if user is None or not verify_password(
            data.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive",
            )

        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is awaiting verification",
            )

        organization = self.organizations.get_active_by_id(user.organization_id)

        if organization is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Organization is inactive",
            )

        return create_access_token(
            user_id=user.id,
            organization_id=user.organization_id,
            role=user.role,
        )
