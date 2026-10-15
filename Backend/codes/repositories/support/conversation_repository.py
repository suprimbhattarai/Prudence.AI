from datetime import datetime, timezone, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from codes.models.support.conversation import Conversation
from codes.models.users.customer_profile import CustomerProfile
from codes.models.users.user import User


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        customer_id: int,
    ) -> Conversation:
        conversation = Conversation(
            customer_id=customer_id,
            title=None,
            status="open",
        )

        self.db.add(conversation)
        self.db.flush()

        return conversation

    def get_by_id_and_user(
        self,
        conversation_id: int,
        user_id: int,
        organization_id: int,
    ) -> Conversation | None:
        statement = (
            select(Conversation)
            .join(
                CustomerProfile,
                Conversation.customer_id == CustomerProfile.id,
            )
            .join(
                User,
                CustomerProfile.user_id == User.id,
            )
            .where(
                Conversation.id == conversation_id,
                User.id == user_id,
                User.organization_id == organization_id,
                Conversation.deleted_at.is_(None),
            )
        )

        return self.db.scalar(statement)

    def get_all_by_user(
        self,
        user_id: int,
        organization_id: int,
    ) -> list[Conversation]:
        statement = (
            select(Conversation)
            .join(
                CustomerProfile,
                Conversation.customer_id == CustomerProfile.id,
            )
            .join(
                User,
                CustomerProfile.user_id == User.id,
            )
            .where(
                User.id == user_id,
                User.organization_id == organization_id,
                Conversation.deleted_at.is_(None),
            )
            .order_by(
                Conversation.updated_at.desc(),
                Conversation.id.desc(),
            )
        )

        return list(self.db.scalars(statement).all())

    def soft_delete(
        self,
        conversation: Conversation,
    ) -> None:
        conversation.deleted_at = datetime.now(timezone.utc)
        self.db.flush()

    def get_for_message_update(
        self,
        conversation_id: int,
        user_id: int,
        organization_id: int,
    ) -> Conversation | None:
        statement = (
            select(Conversation)
            .join(
                CustomerProfile,
                Conversation.customer_id == CustomerProfile.id,
            )
            .join(
                User,
                CustomerProfile.user_id == User.id,
            )
            .where(
                Conversation.id == conversation_id,
                User.id == user_id,
                User.organization_id == organization_id,
                Conversation.deleted_at.is_(None),
            )
            .with_for_update(of=Conversation)
        )

        return self.db.scalar(statement)

    def update_activity(
        self,
        conversation: Conversation,
        initial_title: str,
    ) -> None:
        if conversation.title is None:
            conversation.title = initial_title

        now = datetime.now(timezone.utc)
        previous_updated_at = conversation.updated_at

        if previous_updated_at is not None:
            if previous_updated_at.tzinfo is None:
                previous_updated_at = previous_updated_at.replace(tzinfo=timezone.utc)

            now = max(
                now,
                previous_updated_at + timedelta(microseconds=1),
            )

        conversation.updated_at = now

        self.db.flush()
