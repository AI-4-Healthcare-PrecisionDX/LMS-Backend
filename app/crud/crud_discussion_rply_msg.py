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

class CRUDDiscussionReplyMessage(CRUDBase[DiscussionReplyMessage, DiscussionReplyMessageCreate, DiscussionReplyMessageCreate]):

    def get_reply_by_id(self, db: Session, *, id: uuid.UUID) -> Optional[DiscussionReplyMessage]:
        return db.query(DiscussionReplyMessage).filter(DiscussionReplyMessage.discussion_reply_message_id == id).first()

    def get_replies_by_message(self, db: Session, *, discussion_message_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[DiscussionReplyMessage]:
        return db.query(DiscussionReplyMessage).filter(DiscussionReplyMessage.discussion_message_id == discussion_message_id).offset(skip).limit(limit).all()

    def create_reply(self, db: Session, *, obj_in: DiscussionReplyMessageCreate, user_id: uuid.UUID) -> DiscussionReplyMessage:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise ValueError("User not found")

        db_obj = DiscussionReplyMessage(
            discussion_message_id=obj_in.discussion_message_id,
            user_id=obj_in.user_id,
            discussion_reply_text=obj_in.discussion_reply_text,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_reply(self, db: Session, *, id: uuid.UUID, user_id: uuid.UUID) -> Dict[str, Any]:
        reply = db.query(DiscussionReplyMessage).filter(DiscussionReplyMessage.discussion_reply_message_id == id).first()
        if not reply:
            raise ValueError("Reply not found")

        user = db.query(User).filter(User.user_id == user_id).first()
        if not user or user.user_id != reply.user_id:
            raise ValueError("User not authorized to delete this reply")

        db.delete(reply)
        db.commit()
        return {"message": "Reply deleted successfully"}


# Instantiate CRUDDiscussionReplyMessage for use in API calls
discussion_reply_message = CRUDDiscussionReplyMessage(DiscussionReplyMessage)
