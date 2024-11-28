#app/models/section_exclusive_content.py

from sqlalchemy import  Column, ForeignKey, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class ScenarioPatient(Base):
    __tablename__ = "scenario_patient"
    
    scenario_patient_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    name = Column(String, nullable=True)
    age = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    chief_complaint = Column(String, nullable=True)
    detailed_description = Column(String, nullable=True)
    
    scenario_id = Column(UUID(as_uuid=True), ForeignKey("scenario.scenario_id"))
    scenario = relationship("Scenario", back_populates="scenario_patients")
    
    scenario_examination_findings = relationship("ScenarioExaminationFinding", back_populates="scenario_patient", cascade="all, delete")