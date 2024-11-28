from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class Department(Base):
    department_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    department_name = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    branch_id = Column(UUID(as_uuid=True), ForeignKey("branch.branch_id"))
    branch = relationship("Branch", back_populates="departments")

    template_courses = relationship("TemplateCourse", back_populates="department", cascade="all, delete")
    
    scenarios = relationship("Scenario", back_populates="department", cascade="all, delete")
    