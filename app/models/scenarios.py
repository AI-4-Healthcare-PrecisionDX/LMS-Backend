from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean, JSON, ARRAY
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class Scenario(Base):
    scenario_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )

    scenario_title = Column(String, nullable=True)
    patient_name = Column(String, nullable=True)
    patient_age = Column(String, nullable=True)
    patient_gender = Column(String, nullable=True)
    patient_chief_complaint = Column(String, nullable=True)
    detailed_description = Column(String, nullable=True)
    conversation_example = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    department_id = Column(UUID(as_uuid=True), ForeignKey("department.department_id"))
    department = relationship("Department", back_populates="scenarios")
    
    branch_id = Column(UUID(as_uuid=True), ForeignKey("branch.branch_id"))
    branch = relationship("Branch", back_populates="scenarios")

    scenario_examination_findings = relationship(
        "ScenarioExaminationFinding", back_populates="scenario", cascade="all, delete", uselist=False
    )

    scenario_threads = relationship(
        "ScenarioThread", back_populates="scenario", cascade="all, delete"
    )
