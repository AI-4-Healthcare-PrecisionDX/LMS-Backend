from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.assignment_question import AssignmentQuestion
from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentQuestionCreate, AssignmentQuestionUpdate, AssignmentCreate, AssignmentUpdate, AssignmentQuestionOut,AssignmentOut
from app.models.section import Section


import uuid


class CRUDAssignmentQuestion(CRUDBase[AssignmentQuestion, AssignmentQuestionCreate, AssignmentQuestionUpdate]):
    def get_question_by_id(self, db: Session, *, id: str) -> Optional[AssignmentQuestionOut]:
        return db.query(AssignmentQuestion).filter(AssignmentQuestion.template_course_id == id).first()

    def get_multi(self, db, *, skip = 0, limit = 100):
        return super().get_multi(db, skip=skip, limit=limit)
    
    def create_question(self, db: Session, *, obj_in: AssignmentQuestionCreate,admin_id : uuid) -> AssignmentQuestionOut:
        db_obj = AssignmentQuestion(
            question_type=obj_in.question_type,
            question_text=obj_in.question_text,
            question_answer=obj_in.question_answer,
            marks = obj_in.marks,
            question_description = obj_in.question_description,
            assignment_id = obj_in.assignment_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
        
    def update_question(
        self, db: Session, *, db_obj: AssignmentQuestion, obj_in: AssignmentQuestionUpdate | Dict[str, Any], admin_id: uuid
    ) -> AssignmentQuestion:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    

    def delete_question(self, db: Session, *, id: str) -> Dict[str, Any]:
        question = db.query(AssignmentQuestion).filter(AssignmentQuestion.question_id == id).first()
        if question is None:
            raise ValueError("Question not found")
        
        db.delete(question)
        db.commit()
        return {"message": "Question deleted successfully"}

    

assignment_question = CRUDAssignmentQuestion(AssignmentQuestion)


class CRUDAssignment(CRUDBase[Assignment, AssignmentCreate, AssignmentUpdate]):
    def get_assignment_by_id(self, db: Session, *, id: str) -> Optional[AssignmentOut]:
        return db.query(Assignment).filter(Assignment.assignment_id == id).first()

    def get_multi(self, db, *, skip = 0, limit = 100):
        return super().get_multi(db, skip=skip, limit=limit)
    
    def create_assignment(self, db: Session, *, obj_in: AssignmentCreate,admin_id : uuid) -> AssignmentOut:
        db_obj = Assignment(
            assignment_type=obj_in.assignment_type,
            assignment_title=obj_in.assignment_title,
            assignment_description=obj_in.assignment_description,
            assignment_question_type = obj_in.assignment_question_type,
            number_of_questions = obj_in.number_of_questions,
            total_marks = obj_in.total_marks,
            start_time = obj_in.start_time,
            deadline = obj_in.deadline,
            section_id = obj_in.section_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
        
    def update_assignment(
        self, db: Session, *, db_obj: Assignment, obj_in: AssignmentUpdate | Dict[str, Any], admin_id: uuid
    ) -> Assignment:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    

    def delete_assignment(self, db: Session, *, id: str) -> Dict[str, Any]:
        assignment = db.query(Assignment).filter(Assignment.assignment_id == id).first()
        if assignment is None:
            raise ValueError("Assignment not found")
        
        db.delete(assignment)
        db.commit()
        return {"message": "Assignment deleted successfully"}
    

assignment = CRUDAssignment(Assignment)