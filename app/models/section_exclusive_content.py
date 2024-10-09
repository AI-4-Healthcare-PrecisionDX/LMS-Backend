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
    
    content_type = Column(String, nullable=True)
    content_file = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    section_id = Column(UUID(as_uuid=True), ForeignKey("section.section_id"))
    section = relationship("Section", back_populates="section_exclusive_contents")
