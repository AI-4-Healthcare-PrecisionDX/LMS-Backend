#app/models/section_exclusive_content.py

from sqlalchemy import  Column, ForeignKey, String, DateTime, Boolean,JSON
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class ScenarioExaminationFinding(Base):
    __tablename__ = "scenario_examination_finding"
    
    scenario_examination_finding_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    
    vital_signs = Column(JSON, nullable=True)
    general_appearance = Column(String, nullable=True)
    cardiovascular_findings = Column(String, nullable=True)
    lungs_findings = Column(String, nullable=True)
    additional_findings = Column(JSON, nullable=True)
    
    scenario_patient_id = Column(UUID(as_uuid=True), ForeignKey("scenario_patient.scenario_patient_id"))
    scenario_patient = relationship("ScenarioPatient", back_populates="scenario_examination_findings")
    
    scenario_id = Column(UUID(as_uuid=True), ForeignKey("scenario.scenario_id"))
    scenario = relationship("Scenario", back_populates="scenario_examination_findings")