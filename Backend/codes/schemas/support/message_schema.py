from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class MessageCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=10000,
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        content = value.strip()

        if not content:
            raise ValueError("Message cannot be empty.")

        return content


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    sender_type: str
    content: str
    created_at: datetime
