#app/models/section_exclusive_content.py

from sqlalchemy import  Column, ForeignKey, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class SectionExclusiveContent(Base):
    __tablename__ = "section_exclusive_content"
    
    section_exclusive_content_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    title = Column(String, nullable=True)
    
    description = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    user = relationship("User", back_populates="section_exclusive_contents")
    
    section_id = Column(UUID(as_uuid=True), ForeignKey("section.section_id"))
    section = relationship("Section", back_populates="section_exclusive_contents")
    
    library_item_id = Column(UUID(as_uuid=True), ForeignKey("global_library.library_id"))
    library_item = relationship("GlobalLibrary", back_populates="section_exclusive_content")
    


