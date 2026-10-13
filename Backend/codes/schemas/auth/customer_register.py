from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
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

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return str(value).strip().lower()

    @field_validator("full_name")
    @classmethod
    def normalize_full_name(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 2:
            raise ValueError("Full name is too short")

        return value

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        return value if value else None


class UserRegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: UserRole
    organization_id: int
    is_active: bool
    is_verified: bool
