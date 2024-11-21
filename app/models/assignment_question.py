from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base
from sqlalchemy.dialects.postgresql import ARRAY


class AssignmentQuestion(Base):
    __tablename__ = "assignment_question"
    
    assignment_question_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    question_type = Column(String, nullable=True)
    question_text = Column(String, nullable=False)
    expected_answer = Column(ARRAY(String), nullable=True)
    options_for_mcq = Column(ARRAY(String), nullable=True)
    marks = Column(Integer, nullable=False)
    question_description = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignment.assignment_id"))
    assignment = relationship("Assignment", back_populates="assignment_questions")