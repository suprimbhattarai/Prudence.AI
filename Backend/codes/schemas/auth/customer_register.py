from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from codes.core.enums.user_role import UserRole


class UserRegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr

    password: str = Field(
        min_length=12,
        max_length=128,
    )

    full_name: str = Field(
        min_length=2,
        max_length=150,
    )

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    organization_id: int = Field(gt=0)

    role: Literal[
        UserRole.CUSTOMER,
        UserRole.TECHNICIAN,
    ]

    employee_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()

    @field_validator("full_name")
    @classmethod
    def normalize_full_name(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 2:
            raise ValueError("Full name is too short")

        return value

    @model_validator(mode="after")
    def validate_role_fields(self):
        if self.role == UserRole.TECHNICIAN:
            if not self.employee_code:
                raise ValueError("Employee code is required for technicians")

        if self.role == UserRole.CUSTOMER:
            if self.employee_code is not None:
                raise ValueError("Customers cannot provide employee_code")

        return self


class UserRegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: UserRole
    organization_id: int
    is_active: bool
    is_verified: bool
