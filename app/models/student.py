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
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    user = relationship("User", back_populates="student")
