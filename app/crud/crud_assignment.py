# app/crud/crud_assignment.py
from typing import Any, Dict, Optional, List
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from datetime import datetime
from app.models.assignment_material import AssignmentMaterial
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

    def create_assignment(self, db: Session, *, obj_in: AssignmentCreate) -> Assignment:
        try:
            
            start_time = datetime.strptime(str(obj_in.start_time), "%Y-%m-%dT%H:%M:%S")
            deadline = datetime.strptime(str(obj_in.deadline), "%Y-%m-%dT%H:%M:%S")
            # Validate and create assignment without relationships first
            db_obj = Assignment(
                assignment_type=obj_in.assignment_type,
                assignment_title=obj_in.assignment_title,
                assignment_description=obj_in.assignment_description,
                number_of_questions=obj_in.number_of_questions,
                total_marks=obj_in.total_marks,
                start_time=start_time,
                deadline=deadline,
                section_id=obj_in.section_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(db_obj)
            db.flush()  # This gets us the assignment_id without committing

            # Create assignment materials if provided
            if obj_in.assignment_materials:
                for material_id in obj_in.assignment_materials:
                    material_obj = AssignmentMaterial(
                        library_item_id=material_id,
                        assignment_id=db_obj.assignment_id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(material_obj)

            # Create questions if provided
            if obj_in.questions:
                for question in obj_in.questions:
                    question_obj = AssignmentQuestion(
                        question_type=question.question_type,
                        question_text=question.question_text,
                        expected_answer=question.expected_answer,
                        options_for_mcq=question.options_for_mcq,
                        marks=question.marks,
                        question_description=question.question_description,
                        assignment_id=db_obj.assignment_id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(question_obj)

            db.commit()
            db.refresh(db_obj)
            return db_obj
            
        except Exception as e:
            db.rollback()
            raise e
        

    def update(
        self, db: Session, *, db_obj: Assignment, obj_in: AssignmentUpdate | Dict[str, Any]
    ) -> Assignment:
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)

            # Handle assignment materials if provided
            if "assignment_materials" in update_data:
                # Delete existing materials using a separate query
                db.query(AssignmentMaterial).filter(
                    AssignmentMaterial.assignment_id == db_obj.assignment_id
                ).delete(synchronize_session=False)
                
                # Add new materials
                for material_id in update_data["assignment_materials"]:
                    material_obj = AssignmentMaterial(
                        library_item_id=material_id,
                        assignment_id=db_obj.assignment_id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(material_obj)
                
                del update_data["assignment_materials"]

            # Handle questions if provided
            if "questions" in update_data:
                # Delete existing questions using a separate query
                db.query(AssignmentQuestion).filter(
                    AssignmentQuestion.assignment_id == db_obj.assignment_id
                ).delete(synchronize_session=False)
                
                db.flush()  # Ensure the deletes are processed
                
                # Add new questions
                for question_data in update_data["questions"]:
                    # Convert dict to AssignmentQuestionCreate if necessary
                    if isinstance(question_data, dict):
                        question_data = AssignmentQuestionCreate(**question_data)
                        
                    question_obj = AssignmentQuestion(
                        question_type=question_data.question_type,
                        question_text=question_data.question_text,
                        expected_answer=question_data.expected_answer,
                        options_for_mcq=question_data.options_for_mcq,
                        marks=question_data.marks,
                        question_description=question_data.question_description,
                        assignment_id=db_obj.assignment_id,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(question_obj)
                
                del update_data["questions"]

            # Update the main assignment fields
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            
            db_obj.updated_at = datetime.utcnow()
            db.add(db_obj)
            
            db.commit()
            db.refresh(db_obj)
            
            return db_obj
            
        except Exception as e:
            db.rollback()
            raise e


    def delete_assignment(self, db: Session, *, assignment_id: UUID) -> None:
        try:
            # Begin transaction
            db.begin_nested()
            
            # Get the assignment first to verify it exists
            assignment = db.query(Assignment).filter(
                Assignment.assignment_id == assignment_id
            ).first()
            
            if not assignment:
                raise ValueError("Assignment not found")

            # 1. First delete materials
            db.query(AssignmentMaterial).filter(
                AssignmentMaterial.assignment_id == assignment_id
            ).delete(synchronize_session='fetch')
            db.flush()
            
            # 2. Then delete questions
            db.query(AssignmentQuestion).filter(
                AssignmentQuestion.assignment_id == assignment_id
            ).delete(synchronize_session='fetch')
            db.flush()
            
            # 3. Finally delete the assignment
            db.delete(assignment)
            
            # Commit all changes
            db.commit()
            
        except ValueError as e:
            db.rollback()
            raise e
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error while deleting assignment and related items: {str(e)}")


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