#app/models/global_library.py


from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class GlobalLibrary(Base):
    __tablename__ = "global_library"

    library_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )

    material_type = Column(String, nullable=False)
    material_title = Column(String, nullable=False)
    material_file = Column(String, nullable=False)
    material_description = Column(String, nullable=True)
    author = Column(String, nullable=True)
    visibility = Column(Boolean, default=True)

    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    user = relationship("User", back_populates="global_library_items")

    course_materials = relationship("CourseMaterials", back_populates="library_item")
    
    section_exclusive_content = relationship("SectionExclusiveContent", back_populates="library_item")
    
    assignment_material = relationship("AssignmentMaterial", back_populates="library_item")
