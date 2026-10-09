from sqlalchemy import select
from sqlalchemy.orm import Session

from codes.core.enums.user_role import UserRole
from codes.models.users.user import User
from codes.models.users.customer_profile import CustomerProfile
from codes.models.users.technician_profile import TechnicianProfile


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_technician_by_employee_code(
        self,
        employee_code: str,
    ) -> TechnicianProfile | None:
        return self.db.scalar(
            select(TechnicianProfile).where(
                TechnicianProfile.employee_code == employee_code
            )
        )

    def get_pending_technicians(
        self,
        organization_id: int,
    ):
        statement = (
            select(User, TechnicianProfile)
            .join(
                TechnicianProfile,
                TechnicianProfile.user_id == User.id,
            )
            .where(
                User.organization_id == organization_id,
                User.role == UserRole.TECHNICIAN,
                User.is_verified.is_(False),
            )
            .order_by(User.created_at)
        )

        return self.db.execute(statement).all()

    def get_technician_for_update(
        self,
        user_id: int,
        organization_id: int,
    ) -> User | None:
        statement = (
            select(User)
            .where(
                User.id == user_id,
                User.organization_id == organization_id,
                User.role == UserRole.TECHNICIAN,
            )
            .with_for_update()
        )

        return self.db.scalar(statement)

    def create_user(
        self,
        *,
        email: str,
        hashed_password: str,
        role: UserRole,
        organization_id: int,
        is_verified: bool,
    ) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
            role=role,
            organization_id=organization_id,
            is_active=True,
            is_verified=is_verified,
        )

        self.db.add(user)
        self.db.flush()

        return user

    def create_customer_profile(
        self,
        *,
        user_id: int,
        full_name: str,
        phone: str | None,
    ) -> CustomerProfile:
        profile = CustomerProfile(
            user_id=user_id,
            full_name=full_name,
            phone=phone,
        )

        self.db.add(profile)
        self.db.flush()

        return profile

    def create_technician_profile(
        self,
        *,
        user_id: int,
        full_name: str,
        phone: str | None,
        employee_code: str,
    ) -> TechnicianProfile:
        profile = TechnicianProfile(
            user_id=user_id,
            full_name=full_name,
            phone=phone,
            employee_code=employee_code,
        )

        self.db.add(profile)
        self.db.flush()

        return profile
