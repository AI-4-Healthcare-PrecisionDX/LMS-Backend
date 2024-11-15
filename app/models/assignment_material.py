from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base

class AssignmentMaterial(Base):
    __tablename__ = "assignment_material"
    
    assignment_material_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    title = Column(String, nullable=True)
    
    description = Column(String, nullable=True)
    
    
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    library_item_id = Column(UUID(as_uuid=True), ForeignKey("global_library.library_id"))
    library_item = relationship("GlobalLibrary", back_populates="assignment_material")
    
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignment.assignment_id"))
    assignment = relationship("Assignment", back_populates="assignment_materials")