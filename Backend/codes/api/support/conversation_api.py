from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from codes.database import get_db
from codes.dependencies.authentication import get_current_user
from codes.models.users.user import User

from codes.schemas.support.conversation_schema import (
    ConversationResponse,
)

from codes.services.support.conversation_service import (
    ConversationService,
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    return ConversationService(db).create_conversation(
        current_user=current_user,
    )


@router.get(
    "",
    response_model=list[ConversationResponse],
    status_code=status.HTTP_200_OK,
)
def get_my_conversations(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    return ConversationService(db).get_customer_conversations(
        current_user=current_user,
    )


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_conversation(
    conversation_id: int,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    ConversationService(db).delete_conversation(
        conversation_id=conversation_id,
        current_user=current_user,
    )
