from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class Discussion(Base):
    discussion_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    section_id = Column(UUID(as_uuid=True), ForeignKey("section.section_id"))
    section = relationship("Section", back_populates="discussions")
    
    discussion_messages = relationship("DiscussionMessage", back_populates="discussion")
    
    