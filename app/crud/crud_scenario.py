from typing import Any, Dict, Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.scenarios import Scenario
from app.models.scenario_examination_finding import ScenarioExaminationFinding
from app.models.scenario_thread import ScenarioThread, ScenarioThreadMessage
from app.models.scenario_evaluation import ScenarioEvaluation
from app.models.department import Department
from app.schemas.scenario import (
    ScenarioCreate,
    ScenarioUpdate,
    ScenarioExaminationFindingCreate,
    ScenarioExaminationFindingUpdate,
    ScenarioThreadCreate,
    ScenarioThreadUpdate,
    ScenarioThreadMessageCreate,
    ScenarioThreadMessageUpdate,
    ScenarioData,
    ScenarioEvaluation,
    ScenarioEvaluationCreate,
    ScenarioEvaluationUpdate,
    ScenarioForStudent,
    StudentScenario,
)
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.scenario_evaluation import ScenarioEvaluation  # Import SQLAlchemy model
from app.schemas.scenario import (
    ScenarioEvaluationCreate,
    ScenarioEvaluationUpdate,
)  # Import Pydantic schemas
from uuid import UUID, uuid4


class CRUDScenario(CRUDBase[Scenario, ScenarioCreate, ScenarioUpdate]):
    def get_by_id(self, db: Session, *, scenario_id: str) -> Optional[Scenario]:
        return db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()

    def create_scenario(
        self,
        db: Session,
        *,
        obj_in: ScenarioCreate,
        department_id: UUID,
        branch_id: UUID,
    ) -> Scenario:
        """Create a new scenario using only the fields present in obj_in"""
        # Convert obj_in to dict to easily check for field existence
        obj_data = obj_in.dict(exclude_unset=True)

        # Add department_id to the data
        obj_data["department_id"] = department_id
        obj_data["branch_id"] = branch_id

        # Create scenario instance with only provided fields
        db_obj = Scenario(**obj_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_scenario_with_findings(self, db: Session, *, branch_id: UUID):
        return (
            db.query(Scenario)
            .options(joinedload(Scenario.scenario_examination_findings))
            .filter(Scenario.branch_id == branch_id)
            .all()
        )

    def get_scenario_with_findings_by_scenario_id(
        self, db: Session, *, scenario_id: UUID
    ):
        return (
            db.query(Scenario)
            .options(joinedload(Scenario.scenario_examination_findings))
            .filter(Scenario.scenario_id == scenario_id)
            .first()
        )

    def get_scenario_by_department_id(
        self, db: Session, *, department_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[ScenarioForStudent]:
        scenarios = (
            db.query(Scenario)
            .filter(Scenario.department_id == department_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        if not scenarios:
            return []

        return [
            ScenarioForStudent(
                scenario_id=scenario.scenario_id,
                scenario_title=scenario.scenario_title,
                patient_name=scenario.patient_name,
                patient_age=scenario.patient_age,
                patient_gender=scenario.patient_gender,
                patient_chief_complaint=scenario.patient_chief_complaint,
            )
            for scenario in scenarios
        ]

    def get_student_evaluated_threads(
        self, db: Session, student_id: UUID, department_id: UUID
    ) -> List[StudentScenario]:
        """Get threads that have evaluations"""
        stmt = (
            select(ScenarioThread, Scenario)
            .join(ScenarioThread.scenario)
            .join(Scenario.department)
            .join(ScenarioThread.scenario_evaluation)
            .where(
                ScenarioThread.student_id == student_id,
                Department.department_id == department_id,
            )
        )
        result = db.execute(stmt)

        return [
            StudentScenario(
                thread=thread,
                scenario=ScenarioForStudent(
                    scenario_id=scenario.scenario_id,
                    scenario_title=scenario.scenario_title,
                    patient_name=scenario.patient_name,
                    patient_age=scenario.patient_age,
                    patient_gender=scenario.patient_gender,
                    patient_chief_complaint=scenario.patient_chief_complaint,
                ),
            )
            for thread, scenario in result
        ]

    def get_student_unevaluated_threads(
        self, db: Session, student_id: UUID, department_id: UUID
    ) -> List[StudentScenario]:
        """Get threads that don't have evaluations"""
        stmt = (
            select(ScenarioThread, Scenario)
            .join(ScenarioThread.scenario)
            .join(Scenario.department)
            .outerjoin(ScenarioThread.scenario_evaluation)
            .where(
                ScenarioThread.student_id == student_id,
                Department.department_id == department_id,
                ScenarioEvaluation.scenario_evaluation_id.is_(None),
            )
        )
        result = db.execute(stmt)

        return [
            StudentScenario(
                thread=thread,
                scenario=ScenarioForStudent(
                    scenario_id=scenario.scenario_id,
                    scenario_title=scenario.scenario_title,
                    patient_name=scenario.patient_name,
                    patient_age=scenario.patient_age,
                    patient_gender=scenario.patient_gender,
                    patient_chief_complaint=scenario.patient_chief_complaint,
                ),
            )
            for thread, scenario in result
        ]


scenario = CRUDScenario(Scenario)


class CRUDScenarioExaminationFinding(
    CRUDBase[
        ScenarioExaminationFinding,
        ScenarioExaminationFindingCreate,
        ScenarioExaminationFindingUpdate,
    ]
):
    def get_by_scenario_id(
        self, db: Session, *, scenario_id: str
    ) -> Optional[ScenarioExaminationFinding]:
        return (
            db.query(ScenarioExaminationFinding)
            .filter(ScenarioExaminationFinding.scenario_id == scenario_id)
            .first()
        )

    def create_scenario_examination_findings(
        self,
        db: Session,
        *,
        obj_in: ScenarioExaminationFindingCreate,
        scenario_id: UUID,
    ) -> ScenarioExaminationFinding:
        db_obj = ScenarioExaminationFinding(
            vital_signs=obj_in.vital_signs,
            general_appearance=obj_in.general_appearance,
            cardiovascular_findings=obj_in.cardiovascular_findings,
            lungs_findings=obj_in.lungs_findings,
            additional_findings=obj_in.additional_findings,
            scenario_id=scenario_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


scenario_examination_finding = CRUDScenarioExaminationFinding(
    ScenarioExaminationFinding
)


class CRUDScenarioThread(
    CRUDBase[ScenarioThread, ScenarioThreadCreate, ScenarioThreadUpdate]
):
    def get_by_id(
        self, db: Session, *, scenario_thread_id: UUID
    ) -> Optional[ScenarioThread]:
        return (
            db.query(ScenarioThread)
            .filter(ScenarioThread.scenario_thread_id == scenario_thread_id)
            .first()
        )

    def get_thread_with_messages_by_scenario_id(
        swlf, db: Session, *, scenario_thread_id: UUID
    ):
        return (
            db.query(ScenarioThread)
            .options(joinedload(ScenarioThread.scenario_thread_messages))
            .filter(ScenarioThread.scenario_thread_id == scenario_thread_id)
            .all()
        )

    def get_multi_by_student_id(
        self, db: Session, *, student_id: UUID
    ) -> Optional[ScenarioThread]:
        return (
            db.query(ScenarioThread)
            .filter(ScenarioThread.student_id == student_id)
            .all()
        )

    def create_by_scenario_id(
        self, db: Session, *, scenario_id: UUID, student_id: UUID
    ) -> ScenarioThread:
        # unique name for the thread
        # Get the scenario title to use as the thread name
        scenario = (
            db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()
        )
        thread_name = scenario.scenario_title + " - " + uuid4().hex[:6]
        db_obj = ScenarioThread(
            scenario_id=scenario_id, student_id=student_id, name=thread_name
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


scenario_thread = CRUDScenarioThread(ScenarioThread)


class CRUDScenarioThreadMessage(
    CRUDBase[
        ScenarioThreadMessage, ScenarioThreadMessageCreate, ScenarioThreadMessageUpdate
    ]
):
    def get_multi_by_thread_id(
        self, db: Session, *, scenario_thread_id: UUID
    ) -> Optional[ScenarioThreadMessage]:
        return (
            db.query(ScenarioThreadMessage)
            .filter(ScenarioThreadMessage.scenario_thread_id == scenario_thread_id)
            .order_by(ScenarioThreadMessage.created_at)
            .all()
        )

    def create_by_thread_id(
        self,
        db: Session,
        *,
        scenario_thread_id: str,
        obj_in: ScenarioThreadMessageCreate,
        role: str,
    ) -> ScenarioThreadMessage:
        db_obj = ScenarioThreadMessage(
            role=role, content=obj_in.content, scenario_thread_id=scenario_thread_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


scenario_thread_message = CRUDScenarioThreadMessage(ScenarioThreadMessage)


class CRUDScenarioEvaluation(
    CRUDBase[ScenarioEvaluation, ScenarioEvaluationCreate, ScenarioEvaluationUpdate]
):
    def get_by_thread_id(
        self, db: Session, *, thread_id: UUID
    ) -> Optional[ScenarioEvaluation]:
        return (
            db.query(ScenarioEvaluation)
            .filter(ScenarioEvaluation.thread_id == thread_id)
            .first()
        )

    def create_evaluation(
        self,
        db: Session,
        *,
        obj_in: dict,
    ) -> ScenarioEvaluation:
        """Create a scenario evaluation"""
        # Create SQLAlchemy model instance directly
        db_obj = ScenarioEvaluation(**obj_in)  # This now uses the SQLAlchemy model
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


scenario_evaluation = CRUDScenarioEvaluation(ScenarioEvaluation)
