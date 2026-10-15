from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from codes.core.enums.user_role import UserRole
from codes.models.support.message import Message
from codes.models.users.user import User

from codes.repositories.support.conversation_repository import (
    ConversationRepository,
)
from codes.repositories.support.message_repository import (
    MessageRepository,
)
from codes.services.support.conversation_title_service import (
    ConversationTitleService,
)


class MessageService:
    def __init__(self, db: Session):
        self.db = db
        self.conversation_repository = ConversationRepository(db)
        self.message_repository = MessageRepository(db)

    def create_customer_message(
        self,
        conversation_id: int,
        content: str,
        current_user: User,
    ) -> Message:
        if current_user.role != UserRole.CUSTOMER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customers can send customer messages.",
            )

        try:
            conversation = self.conversation_repository.get_for_message_update(
                conversation_id=conversation_id,
                user_id=current_user.id,
                organization_id=current_user.organization_id,
            )

            if conversation is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found.",
                )

            if conversation.status != "open":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cannot send messages to a closed conversation.",
                )

            message = self.message_repository.create(
                conversation_id=conversation.id,
                sender_type="customer",
                content=content,
            )

            if conversation.title is None:
                conversation.title = ConversationTitleService.generate_initial_title(
                    content
                )

            now = datetime.now(timezone.utc)
            previous_updated_at = conversation.updated_at

            if previous_updated_at is not None:
                if previous_updated_at.tzinfo is None:
                    previous_updated_at = previous_updated_at.replace(
                        tzinfo=timezone.utc
                    )

                now = max(
                    now,
                    previous_updated_at + timedelta(microseconds=1),
                )

            conversation.updated_at = now

            self.db.commit()
            self.db.refresh(message)

            return message

        except Exception:
            self.db.rollback()
            raise

    def get_conversation_messages(
        self,
        conversation_id: int,
        current_user: User,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Message]:
        if current_user.role != UserRole.CUSTOMER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customers can view customer conversations.",
            )

        conversation = self.conversation_repository.get_by_id_and_user(
            conversation_id=conversation_id,
            user_id=current_user.id,
            organization_id=current_user.organization_id,
        )

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found.",
            )

        return self.message_repository.get_by_conversation(
            conversation_id=conversation.id,
            limit=limit,
            offset=offset,
        )
