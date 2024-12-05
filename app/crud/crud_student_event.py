# app/crud/crud_student_event.py

from typing import List
from sqlalchemy.orm import Session
from app.models.student_event import StudentEvent
from app.schemas.student_event import StudentEventCreate, StudentEventUpdate
from app.crud.base import CRUDBase
from uuid import UUID


class CRUDStudentEvent(CRUDBase[StudentEvent, StudentEventCreate, StudentEventUpdate]):
    def create_student_event(self, db: Session, *, obj_in: StudentEventCreate, student_id: str) -> StudentEvent:
        """
        Create a new event for a student.
        """
        db_obj = StudentEvent(**obj_in.dict(), student_id=student_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_student_event_by_id(self, db: Session, event_id: UUID) -> StudentEvent | None:
        """
        Retrieve a student event by its event_id.
        """
        return db.query(StudentEvent).filter(StudentEvent.event_id == event_id).first()

    def update_student_event(
        self, db: Session, *, db_obj: StudentEvent, obj_in: StudentEventUpdate
    ) -> StudentEvent:
        """
        Update a student event.
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_student_event(self, db: Session, *, event_id: int) -> StudentEvent | None:
        """
        Remove a student event by its event_id.
        """
        obj = db.query(StudentEvent).filter(StudentEvent.event_id == event_id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj




student_event = CRUDStudentEvent(StudentEvent)
