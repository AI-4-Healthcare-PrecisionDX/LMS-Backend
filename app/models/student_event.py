# app/models/student_event.py

from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class StudentEvent(Base):
    event_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    topics = Column(ARRAY(String), nullable=True)  # arr
    date = Column(DateTime, nullable=False)
    link = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


    student_id = Column(UUID(as_uuid=True), ForeignKey("student.student_id"), nullable=False)
    

    student = relationship("Student", back_populates="student_event")
