from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base

class Assignment(Base):
    assignment_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    assignment_type = Column(String, nullable=False) # traditional / ai generated
    assignment_title = Column(String, nullable=False)
    assignment_description = Column(String, nullable=True)
    assignment_question_type = Column(String, nullable=False)
    number_of_questions = Column(Integer, nullable=False)
    total_marks = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    section_id = Column(UUID(as_uuid=True), ForeignKey("section.section_id"))
    section = relationship("Section", back_populates="assignments")
    
    assignment_materials = relationship("AssignmentMaterial", back_populates="assignment")
    
    assignment_questions = relationship("AssignmentQuestion", back_populates="assignment")
    
    
    assignment_submissions = relationship("AssignmentSubmission", back_populates="assignment")