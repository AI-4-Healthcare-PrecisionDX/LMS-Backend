from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base

class Announcement(Base):
    announcement_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    announcement_title = Column(String, nullable=False)
    announcement_description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    section_id = Column(UUID(as_uuid=True), ForeignKey("section.section_id"))
    section = relationship("Section", back_populates="announcements")
    
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teacher.teacher_id"))
    teacher = relationship("Teacher", back_populates="announcements")