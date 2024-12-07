from sqlalchemy import Column, ForeignKey, String, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
import uuid
import datetime

from app.db.base_class import Base


class ScenarioThread(Base):
    __tablename__ = "scenario_thread"

    scenario_thread_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    scenario_id = Column(UUID(as_uuid=True), ForeignKey("scenario.scenario_id"))
    scenario = relationship("Scenario", back_populates="scenario_threads")

    student_id = Column(UUID(as_uuid=True), ForeignKey("student.student_id"))
    student = relationship("Student", back_populates="scenario_threads")

    scenario_thread_messages = relationship(
        "ScenarioThreadMessage", back_populates="scenario_thread", cascade="all, delete"
    )

    scenario_evaluation = relationship(
        "ScenarioEvaluation",
        back_populates="thread",
        cascade="all, delete",
        uselist=False,
    )


class ScenarioThreadMessage(Base):
    __tablename__ = "scenario_thread_message"

    scenario_thread_message_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )

    role = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    scenario_thread_id = Column(
        UUID(as_uuid=True), ForeignKey("scenario_thread.scenario_thread_id")
    )
    scenario_thread = relationship(
        "ScenarioThread", back_populates="scenario_thread_messages"
    )
