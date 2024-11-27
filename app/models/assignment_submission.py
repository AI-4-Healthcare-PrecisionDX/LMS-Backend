from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class AssignmentSubmission(Base):
    __tablename__ = "assignment_submission"
    
    assignment_submission_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    total_marks_after_eval = Column(Integer, nullable=True, default=0)
    evaluated = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignment.assignment_id"))
    assignment = relationship("Assignment", back_populates="assignment_submissions")
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("student.student_id"))
    student = relationship("Student", back_populates="assignment_submissions")
    
    assignment_submission_answers = relationship("AssignmentSubmissionAnswer", back_populates="assignment_submission", cascade="all, delete")