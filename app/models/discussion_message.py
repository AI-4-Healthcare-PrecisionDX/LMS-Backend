from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class DiscussionMessage(Base):
    __tablename__ = "discussion_message"
    
    discussion_message_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    discussion_text = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    discussion_id = Column(UUID(as_uuid=True), ForeignKey("discussion.discussion_id"))
    discussion = relationship("Discussion", back_populates="discussion_messages")
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    user = relationship("User", back_populates="discussion_messages")
    
    
    discussion_reply_messages = relationship("DiscussionReplyMessage", back_populates="discussion_message", cascade="all, delete")
    