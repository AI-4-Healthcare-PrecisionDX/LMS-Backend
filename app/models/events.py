from sqlalchemy import Boolean, Column, String, DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID,ARRAY
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class Events(Base):
    event_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    event_title = Column(String, nullable=False)
    event_topics = Column(ARRAY(String), nullable=True, default=list) 
    event_description = Column(String, nullable=True)
    event_link = Column(String, nullable=True)
    event_date = Column(DateTime, nullable=True)
    is_completed = Column(Boolean,nullable=False, default=False)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("student.student_id"))
    student = relationship("Student", back_populates="events")
    
    

    