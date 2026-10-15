from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from codes.core.enums.user_role import UserRole
from codes.models.support.conversation import Conversation
from codes.models.users.user import User
from codes.models.users.customer_profile import CustomerProfile

from codes.repositories.support.conversation_repository import (
    ConversationRepository,
)

from sqlalchemy import update

from codes.models.support.complaint import Complaint


class ConversationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ConversationRepository(db)

    def create_conversation(
        self,
        current_user: User,
    ):
        if current_user.role != UserRole.CUSTOMER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customers can start conversations.",
            )

        customer_profile = self.db.scalar(
            select(CustomerProfile).where(CustomerProfile.user_id == current_user.id)
        )

        if customer_profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer profile not found.",
            )

        try:
            conversation = self.repository.create(
                customer_id=customer_profile.id,
            )

            self.db.commit()
            self.db.refresh(conversation)

            return conversation

        except Exception:
            self.db.rollback()
            raise

    def get_customer_conversations(
        self,
        current_user: User,
    ) -> list[Conversation]:
        if current_user.role != UserRole.CUSTOMER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customers can view customer conversations.",
            )

        return self.repository.get_all_by_user(
            user_id=current_user.id,
            organization_id=current_user.organization_id,
        )

    def delete_conversation(
        self,
        conversation_id: int,
        current_user: User,
    ) -> None:
        if current_user.role != UserRole.CUSTOMER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only customers can delete conversations.",
            )

        conversation = self.repository.get_by_id_and_user(
            conversation_id=conversation_id,
            user_id=current_user.id,
            organization_id=current_user.organization_id,
        )

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found.",
            )

        try:
            self.repository.soft_delete(conversation)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
