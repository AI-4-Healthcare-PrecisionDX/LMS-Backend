from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class TemplateCourse(Base):
    __tablename__ = "template_course"

    template_course_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    template_name = Column(String, nullable=False)
    template_description = Column(String, nullable=True)
    template_year = Column(String, nullable=True)
    course_outline = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    admin_id = Column(UUID(as_uuid=True), ForeignKey("admin.admin_id"))
    admin = relationship("Admin", back_populates="template_courses")
    
    department_id = Column(UUID(as_uuid=True), ForeignKey("department.department_id"))
    department = relationship("Department", back_populates="template_courses")
    
    sections = relationship("Section", back_populates="template_course")
    
    course_materials = relationship("CourseMaterials", back_populates="template_course")