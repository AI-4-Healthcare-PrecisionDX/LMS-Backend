#app/models/template_course_materials.py

from sqlalchemy import  Column, ForeignKey, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class CourseMaterials(Base):
    __tablename__ = "course_materials"
    
    course_material_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    user = relationship("User", back_populates="course_materials")
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    template_course_id = Column(UUID(as_uuid=True), ForeignKey("template_course.template_course_id"))
    template_course = relationship("TemplateCourse", back_populates="course_materials")
    
    library_item_id = Column(UUID(as_uuid=True), ForeignKey("global_library.library_id"))
    library_item = relationship("GlobalLibrary", back_populates="course_materials")
    