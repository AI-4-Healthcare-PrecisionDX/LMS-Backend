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
    
    submitted_file = Column(String, nullable=True)
    grading = Column(String, nullable=True) #CharField(10, choices=[('Not Graded', 'Not Graded'), ('Graded', 'Graded')])
    grade = Column(Integer, nullable=True)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("student.student_id"))
    student = relationship("Student", back_populates="assignment_submissions")
    
    assignment_id = Column(UUID(as_uuid=True), ForeignKey("assignment.assignment_id"))
    assignment = relationship("Assignment", back_populates="assignment_submissions")
    
    