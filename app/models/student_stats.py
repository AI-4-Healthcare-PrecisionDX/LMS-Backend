from sqlalchemy import  Column, ForeignKey, String, DateTime, Boolean,Integer
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class StudentStats(Base):
    __tablename__ = "student_stats"
    
    student_stats_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    exam_name = Column(String, nullable=False)
    full_marks = Column(Integer, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("student.student_id"))
    student = relationship("Student", back_populates="student_stats")
    
    section_id = Column(UUID(as_uuid=True), ForeignKey("section.section_id"))
    section = relationship("Section", back_populates="student_stats")
    
    