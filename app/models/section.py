#app/models/section.py

from sqlalchemy import  Column, ForeignKey, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class Section(Base):
    section_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    section_name = Column(String, nullable=False)
    section_code = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teacher.teacher_id"))
    teacher = relationship("Teacher", back_populates="sections")
    
    template_course_id = Column(UUID(as_uuid=True), ForeignKey("template_course.template_course_id"))
    template_course = relationship("TemplateCourse", back_populates="sections")
    
    section_exclusive_contents = relationship("SectionExclusiveContent", back_populates="section")
    
    assignments = relationship("Assignment", back_populates="section")
    
    student_stats = relationship("StudentStats", back_populates="section")
    
    inboxes = relationship("Inbox", back_populates="section")
    
    discussions = relationship("Discussion", back_populates="section")