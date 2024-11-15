from sqlalchemy import Boolean, Column, String, DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class Notes(Base):
    note_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    note_title = Column(String, nullable=False)
    note_content = Column(String, nullable=True)
    note_markdown_content = Column(String, nullable=True)
    note_teacher = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("student.student_id"))
    student = relationship("Student", back_populates="notes")
    
