from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey,Integer,ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class AssignmentSubmissionAnswer(Base):
    __tablename__ = "assignment_submission_answer"
    
    assignment_submission_answer_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    answers = Column(ARRAY(String), nullable=False)
    
    total_marks_after_eval = Column(Integer, nullable=False, default=0)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    assignment_submission_id = Column(UUID(as_uuid=True), ForeignKey("assignment_submission.assignment_submission_id"))
    assignment_submission = relationship("AssignmentSubmission", back_populates="assignment_submission_answers")
    
    question_id = Column(UUID(as_uuid=True), ForeignKey("assignment_question.assignment_question_id"))
    question = relationship("AssignmentQuestion", back_populates="assignment_submission_answer")
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("student.student_id"))
    student = relationship("Student", back_populates="assignment_submission_answers")