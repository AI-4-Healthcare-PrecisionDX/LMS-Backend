from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.discussion_message import DiscussionMessage
from app.models.discussion_reply_message import DiscussionReplyMessage
from app.schemas.discussion_message import DiscussionMessageCreate
from app.schemas.discussion_reply_message import DiscussionReplyMessageCreate
from app.models.user import User
import uuid
from datetime import datetime




class CRUDDiscussionMessage(CRUDBase[DiscussionMessage, DiscussionMessageCreate, DiscussionMessageCreate]):
    
    def get_message_by_id(self, db: Session, *, id: uuid.UUID) -> Optional[DiscussionMessage]:
        return db.query(DiscussionMessage).filter(DiscussionMessage.discussion_message_id == id).first()

    def get_messages_by_discussion(self, db: Session, *, discussion_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[DiscussionMessage]:
        return db.query(DiscussionMessage).filter(DiscussionMessage.discussion_id == discussion_id).offset(skip).limit(limit).all()

    def create_message(self, db: Session, *, obj_in: DiscussionMessageCreate, user_id: uuid.UUID) -> DiscussionMessage:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise ValueError("User not found")

        db_obj = DiscussionMessage(
            discussion_id=obj_in.discussion_id,
            user_id=obj_in.user_id,
            discussion_text=obj_in.discussion_text,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_message(self, db: Session, *, id: uuid.UUID, user_id: uuid.UUID) -> Dict[str, Any]:
        message = db.query(DiscussionMessage).filter(DiscussionMessage.discussion_message_id == id).first()
        if not message:
            raise ValueError("Message not found")

        user = db.query(User).filter(User.user_id == user_id).first()
        if not user or user.user_id != message.user_id:
            raise ValueError("User not authorized to delete this message")

        db.delete(message)
        db.commit()
        return {"message": "Message deleted successfully"}


# Instantiate CRUDDiscussionMessage for use in API calls
discussion_message = CRUDDiscussionMessage(DiscussionMessage)


