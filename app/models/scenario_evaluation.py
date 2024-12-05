# app/models/scenario_evaluation.py

from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean, JSON, Float
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class ScenarioEvaluation(Base):
    __tablename__ = "scenario_evaluation"

    scenario_evaluation_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )

    conversation_relevance_of_replies_score = Column(Float, nullable=True)
    conversation_medical_accuracy_of_replies_score = Column(Float, nullable=True)
    conversation_communication_clarity_score = Column(Float, nullable=True)
    conversation_empathy_and_professionalism_score = Column(Float, nullable=True)
    conversation_constructive_feedback = Column(String, nullable=True)
    
    diagnosis_relevance_score = Column(Float, nullable=True)
    diagnosis_accuracy_score = Column(Float, nullable=True)
    diagnosis_constructive_feedback = Column(String, nullable=True)
    
    treatment_relevance_score = Column(Float, nullable=True)
    treatment_effectiveness_score = Column(Float, nullable=True)
    treatment_constructive_feedback = Column(String, nullable=True)
    
    notes_clarity_score = Column(Float, nullable=True)
    notes_completeness_score = Column(Float, nullable=True)
    notes_constructive_feedback = Column(String, nullable=True)
    
    time_management = Column(String, nullable=True)
    other_observations = Column(String, nullable=True)
    
    overall_score = Column(Float, nullable=True)
    overall_constructive_feedback = Column(String, nullable=True)
    additional_notes = Column(String, nullable=True)
    
    thread_id = Column(UUID(as_uuid=True), ForeignKey("scenario_thread.scenario_thread_id"))
    thread = relationship("ScenarioThread", back_populates="scenario_evaluation")