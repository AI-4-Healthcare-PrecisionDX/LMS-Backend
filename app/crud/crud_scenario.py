from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.scenarios import Scenario
from app.models.scenario_examination_finding import ScenarioExaminationFinding
from app.models.scenario_thread import ScenarioThread, ScenarioThreadMessage

from app.schemas.scenario import (
    ScenarioCreate,
    ScenarioUpdate,
    ScenarioExaminationFindingCreate,
    ScenarioExaminationFindingUpdate,
    ScenarioThreadCreate,
    ScenarioThreadUpdate,
    ScenarioThreadMessageCreate,
    ScenarioThreadMessageUpdate,
)


class CRUDScenario(CRUDBase[Scenario, ScenarioCreate, ScenarioUpdate]):
    def get_by_id(self, db: Session, *, scenario_id: str) -> Optional[Scenario]:
        return db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()


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


scenario_examination_finding = CRUDScenarioExaminationFinding(
    ScenarioExaminationFinding
)


class CRUDScenarioThread(
    CRUDBase[ScenarioThread, ScenarioThreadCreate, ScenarioThreadUpdate]
):
    def get_by_id(
        self, db: Session, *, scenario_thread_id: str
    ) -> Optional[ScenarioThread]:
        return (
            db.query(ScenarioThread)
            .filter(ScenarioThread.scenario_thread_id == scenario_thread_id)
            .first()
        )

    def create_by_scenario_id(self, db: Session, *, scenario_id: str) -> ScenarioThread:
        db_obj = ScenarioThread(scenario_id=scenario_id)
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
        self, db: Session, *, scenario_thread_id: str
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
        role: str
    ) -> ScenarioThreadMessage:
        db_obj = ScenarioThreadMessage(
            role=role, content=obj_in.content, scenario_thread_id=scenario_thread_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


scenario_thread_message = CRUDScenarioThreadMessage(ScenarioThreadMessage)
