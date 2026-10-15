from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from codes.database import get_db
from codes.dependencies.authentication import get_current_user
from codes.models.users.user import User

from codes.schemas.support.message_schema import (
    MessageCreate,
    MessageResponse,
)

from codes.services.support.message_service import (
    MessageService,
)

router = APIRouter(
    prefix="/conversations",
    tags=["Messages"],
)


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    conversation_id: int,
    message_data: MessageCreate,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    return MessageService(db).create_customer_message(
        conversation_id=conversation_id,
        content=message_data.content,
        current_user=current_user,
    )


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
    status_code=status.HTTP_200_OK,
)
def get_conversation_messages(
    conversation_id: int,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    limit: Annotated[
        int,
        Query(ge=1, le=100),
    ] = 50,
    offset: Annotated[
        int,
        Query(ge=0),
    ] = 0,
):
    return MessageService(db).get_conversation_messages(
        conversation_id=conversation_id,
        current_user=current_user,
        limit=limit,
        offset=offset,
    )
