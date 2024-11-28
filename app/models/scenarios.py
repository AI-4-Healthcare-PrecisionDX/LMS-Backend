#app/models/section_exclusive_content.py

from sqlalchemy import  Column, ForeignKey, String, DateTime, Boolean,JSON
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
    conversation = Column(JSON, nullable=True)
    
    department_id = Column(UUID(as_uuid=True), ForeignKey("department.department_id"))
    department = relationship("Department", back_populates="scenarios")
    
    scenario_patients = relationship("ScenarioPatient", back_populates="scenario", cascade="all, delete")
    
    scenario_examination_findings = relationship("ScenarioExaminationFinding", back_populates="scenario", cascade="all, delete")