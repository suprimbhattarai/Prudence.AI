from sqlalchemy.orm import Session

from codes.models.support.message import Message

from sqlalchemy import select


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        conversation_id: int,
        sender_type: str,
        content: str,
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            sender_type=sender_type,
            content=content,
        )

        self.db.add(message)
        self.db.flush()

        return message

    # Add inside MessageRepository

    def get_by_conversation(
        self,
        conversation_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Message]:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(
                Message.created_at.asc(),
                Message.id.asc(),
            )
            .limit(limit)
            .offset(offset)
        )

        return list(self.db.scalars(statement).all())
