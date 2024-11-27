#app/models/student.py
from sqlalchemy import  Column, ForeignKey, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class Student(Base):
    student_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    metric_id = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    user = relationship("User", back_populates="student")
    
    
    student_stats = relationship("StudentStats", back_populates="student", cascade="all, delete")
    
    inboxes = relationship("Inbox", back_populates="student", cascade="all, delete")
    

    student_event = relationship("StudentEvent", back_populates="student", cascade="all, delete")

    assignment_submissions = relationship("AssignmentSubmission", back_populates="student", cascade="all, delete")
    
    notes = relationship("Notes", back_populates="student", cascade="all, delete")
    
    assignment_submission_answers = relationship("AssignmentSubmissionAnswer", back_populates="student", cascade="all, delete")