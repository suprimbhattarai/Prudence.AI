from pydantic import BaseModel, ConfigDict, EmailStr

from codes.core.enums.user_role import UserRole


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class CurrentUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: UserRole
    organization_id: int
    is_active: bool
    is_verified: bool
