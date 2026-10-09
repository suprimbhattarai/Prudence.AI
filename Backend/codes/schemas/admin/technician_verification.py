from pydantic import BaseModel, ConfigDict, EmailStr


class TechnicianVerificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    organization_id: int
    is_verified: bool


class PendingTechnicianResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    employee_code: str
    organization_id: int
