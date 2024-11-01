# app/crud/crud_assignment.py
from typing import Any, Dict, Optional, List
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.assignment import Assignment
from app.models.assignment_question import AssignmentQuestion
from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentQuestionCreate,
    AssignmentQuestionUpdate,
)

class CRUDAssignment(CRUDBase[Assignment, AssignmentCreate, AssignmentUpdate]):
    def get_by_id(self, db: Session, *, id: UUID) -> Optional[Assignment]:
        return (
            db.query(Assignment)
            .filter(Assignment.assignment_id == id)
            .options(joinedload(Assignment.assignment_questions))
            .first()
        )

    def get_by_section(
        self, db: Session, *, section_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Assignment]:
        return (
            db.query(Assignment)
            .filter(Assignment.section_id == section_id)
            .options(joinedload(Assignment.assignment_questions))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: AssignmentCreate) -> Assignment:
        try:
            db_obj = Assignment(
            assignment_type=obj_in.assignment_type,
            assignment_title=obj_in.assignment_title,
            assignment_description=obj_in.assignment_description,
            assignment_question_type=obj_in.assignment_question_type,
            number_of_questions=obj_in.number_of_questions,
            total_marks=obj_in.total_marks,
            start_time=obj_in.start_time,
            deadline=obj_in.deadline,
            section_id=obj_in.section_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            raise ValueError(f"An error occurred while creating assignment: {str(e)}")
        

    def update(
        self, db: Session, *, db_obj: Assignment, obj_in: AssignmentUpdate | Dict[str, Any]
    ) -> Assignment:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        update_data["updated_at"] = datetime.utcnow()
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def delete(self, db: Session, *, id: UUID) -> None:
        # First delete all associated questions
        db.query(AssignmentQuestion).filter(
            AssignmentQuestion.assignment_id == id
        ).delete()
        
        # Then delete the assignment
        assignment = db.query(Assignment).filter(Assignment.assignment_id == id).first()
        if assignment:
            db.delete(assignment)
            db.commit()

class CRUDAssignmentQuestion(CRUDBase[AssignmentQuestion, AssignmentQuestionCreate, AssignmentQuestionUpdate]):
    def get_by_id(self, db: Session, *, id: UUID) -> Optional[AssignmentQuestion]:
        return db.query(AssignmentQuestion).filter(
            AssignmentQuestion.assignment_question_id == id
        ).first()

    def get_by_assignment(
        self, db: Session, *, assignment_id: UUID
    ) -> List[AssignmentQuestion]:
        return db.query(AssignmentQuestion).filter(
            AssignmentQuestion.assignment_id == assignment_id
        ).all()

    def create(
        self, db: Session, *, obj_in: AssignmentQuestionCreate, assignment_id: UUID
    ) -> AssignmentQuestion:
        db_obj = AssignmentQuestion(
            question_type=obj_in.question_type,
            question_text=obj_in.question_text,
            expected_answer=obj_in.expected_answer,
            options_for_mcq=obj_in.options_for_mcq,
            marks=obj_in.marks,
            question_description=obj_in.question_description,
            assignment_id=assignment_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, 
        db: Session, 
        *, 
        db_obj: AssignmentQuestion,
        obj_in: AssignmentQuestionUpdate | Dict[str, Any]
    ) -> AssignmentQuestion:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        update_data["updated_at"] = datetime.utcnow()
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def create_multiple(
        self, db: Session, *, questions_in: List[AssignmentQuestionCreate], assignment_id: UUID
    ) -> List[AssignmentQuestion]:
        questions = []
        for question_in in questions_in:
            db_obj = AssignmentQuestion(
                question_type=question_in.question_type,
                question_text=question_in.question_text,
                expected_answer=question_in.expected_answer,
                options_for_mcq=question_in.options_for_mcq,
                marks=question_in.marks,
                question_description=question_in.question_description,
                assignment_id=assignment_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(db_obj)
            questions.append(db_obj)
        
        db.commit()
        for question in questions:
            db.refresh(question)
        return questions

    def delete(self, db: Session, *, id: UUID) -> None:
        question = db.query(AssignmentQuestion).filter(
            AssignmentQuestion.assignment_question_id == id
        ).first()
        if question:
            db.delete(question)
            db.commit()

assignment = CRUDAssignment(Assignment)
assignment_question = CRUDAssignmentQuestion(AssignmentQuestion)