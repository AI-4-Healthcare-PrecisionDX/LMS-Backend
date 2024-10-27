#app/models/template_course_access.py

from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class TemplateCourseAccess(Base):
    __tablename__ = "template_course_access"
    
    template_course_access_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    template_course_id = Column(UUID(as_uuid=True), ForeignKey("template_course.template_course_id"))
    template_course = relationship("TemplateCourse", back_populates="template_course_access")
    
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teacher.teacher_id"))
    teacher = relationship("Teacher", back_populates="template_course_access")
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)