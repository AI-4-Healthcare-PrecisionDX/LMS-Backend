from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class Branch(Base):
    branch_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    branch_name = Column(String, nullable=False)
    branch_address = Column(String, nullable=False)
    branch_contact = Column(String, nullable=False)
    branch_email = Column(String, nullable=False)
    branch_website = Column(String, nullable=True)
    branch_fax = Column(String, nullable=True)
    branch_is_active = Column(Boolean(), default=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    institution_id = Column(
        UUID(as_uuid=True), ForeignKey("institution.institution_id")
    )
    institution = relationship("Institution", back_populates="branches")
    departments = relationship("Department", back_populates="branch")
    users = relationship("User", back_populates="branch")
    template_courses = relationship("TemplateCourse", back_populates="branch")
    scenarios = relationship("Scenario", back_populates="branch")
