# app/api/api_v1/endpoints/assignment.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/create-assignment", response_model=schemas.Assignment)
def create_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_in: schemas.AssignmentCreate,
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user)
) -> Any:
    

    # Verify section exists and teacher has access
    section = crud.section.get_section_by_id(db=db, id=assignment_in.section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    if not crud.section.check_section_owner(
        db=db,
        section_id=section.section_id,
        teacher_id=current_teacher.teacher_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to remove content from this section"
        )

    try:
        return crud.assignment.create_assignment(db=db, obj_in=assignment_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    

@router.get("/section/{section_id}/assignments", response_model=List[schemas.Assignment])
def read_section_assignments(
    section_id: UUID,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get all assignments for a section.
    """
    # Verify section exists and user has access
    section = crud.section.get_section_by_id(db=db, id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    if current_user.role == "teacher":
        teacher = crud.user.get_teacher_by_user_id(db=db, id=current_user.user_id)
        if not teacher or section.teacher_id != teacher.teacher_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to view assignments in this section"
            )

    return crud.assignment.get_by_section(db=db, section_id=section_id, skip=skip, limit=limit)

@router.get("/{assignment_id}", response_model=schemas.Assignment)
def read_assignment(
    assignment_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get assignment by ID.
    """
    assignment = crud.assignment.get_by_id(db=db, id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Verify user has access
    section = crud.section.get_section_by_id(db=db, id=assignment.section_id)
    if current_user.role == "teacher":
        teacher = crud.user.get_teacher_by_user_id(db=db, id=current_user.user_id)
        if not teacher or section.teacher_id != teacher.teacher_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to view this assignment"
            )

    return assignment

@router.put("/{assignment_id}", response_model=schemas.Assignment)
def update_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_id: UUID,
    assignment_in: schemas.AssignmentUpdate,
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user)
) -> Any:
    """
    Update an assignment including its materials and questions.
    """
    try:
        # Get the existing assignment
        assignment = crud.assignment.get_by_id(db=db, id=assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        # Verify teacher has access
        section = crud.section.get_section_by_id(db=db, id=assignment.section_id)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        teacher = crud.user.get_teacher_by_user_id(db=db, id=current_teacher.user_id)
        if not teacher or section.teacher_id != teacher.teacher_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to update this assignment"
            )

        # Validate the total marks matches sum of question marks if questions are being updated
        if assignment_in.questions:
            total_marks = sum(q.marks for q in assignment_in.questions)
            if assignment_in.total_marks is not None:
                if total_marks != assignment_in.total_marks:
                    raise HTTPException(
                        status_code=400,
                        detail="Total marks must match sum of individual question marks"
                    )
            else:
                assignment_in.total_marks = total_marks

        # Validate number of questions if being updated
        if assignment_in.questions:
            num_questions = len(assignment_in.questions)
            if assignment_in.number_of_questions is not None:
                if num_questions != assignment_in.number_of_questions:
                    raise HTTPException(
                        status_code=400,
                        detail="Number of questions must match actual question count"
                    )
            else:
                assignment_in.number_of_questions = num_questions

        # Update the assignment
        updated_assignment = crud.assignment.update(
            db=db,
            db_obj=assignment,
            obj_in=assignment_in
        )
        return updated_assignment
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    

@router.delete("/{assignment_id}", response_model=schemas.DeleteAssignmentResponse)
def delete_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_id: UUID,
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user)
) -> Any:
    """
    Delete an assignment and all related content.
    """
    try:
        # Get assignment for permission check
        assignment = crud.assignment.get_by_id(db=db, id=assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        # Verify teacher has access
        if not crud.section.check_section_owner(
        db=db,
        section_id=assignment.section_id,
        teacher_id=current_teacher.teacher_id):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to remove content from this section"
            )
        
        # Delete the assignment and get the result
        crud.assignment.delete_assignment(db=db, assignment_id=assignment_id)
        
        # Return the response directly as a dict
        return {
            "message": "Assignment and related content deleted successfully",
            "details": {
                "assignment_id": str(assignment_id)
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the assignment: {str(e)}"
        )
        

# Assignment Questions Endpoints
@router.post("/{assignment_id}/questions", response_model=schemas.AssignmentQuestionInDB)
def create_question(
    *,
    db: Session = Depends(deps.get_db),
    assignment_id: UUID,
    question_in: schemas.AssignmentQuestionCreate,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create new question for an assignment.
    """
    try:
        # Verify assignment exists and teacher has access
        assignment = crud.assignment.get_by_id(db=db, id=assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        section = crud.section.get_section_by_id(db=db, id=assignment.section_id)
        if current_user.role != "teacher":
            raise HTTPException(status_code=403, detail="Only teachers can create questions")

        teacher = crud.user.get_teacher_by_user_id(db=db, id=current_user.user_id)
        if not teacher or section.teacher_id != teacher.teacher_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to create questions for this assignment"
            )

        return crud.assignment_question.create(db=db, obj_in=question_in, assignment_id=assignment_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{assignment_id}/questions/batch", response_model=List[schemas.AssignmentQuestionInDB])
def create_questions_batch(
    *,
    db: Session = Depends(deps.get_db),
    assignment_id: UUID,
    questions_in: List[schemas.AssignmentQuestionCreate],
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create multiple questions for an assignment in a single request.
    """
    try:
        # Verify assignment exists and teacher has access
        assignment = crud.assignment.get_by_id(db=db, id=assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")

        section = crud.section.get_section_by_id(db=db, id=assignment.section_id)
        if current_user.role != "teacher":
            raise HTTPException(status_code=403, detail="Only teachers can create questions")

        teacher = crud.user.get_teacher_by_user_id(db=db, id=current_user.user_id)
        if not teacher or section.teacher_id != teacher.teacher_id:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to create questions for this assignment"
            )

        return crud.assignment_question.create_multiple(
            db=db, 
            questions_in=questions_in, 
            assignment_id=assignment_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/question/{question_id}", response_model=schemas.AssignmentQuestionInDB)
def read_question(
    question_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get question by ID.
    """
    try:
        question = crud.assignment_question.get_by_id(db=db, id=question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Verify user has access
        assignment = crud.assignment.get_by_id(db=db, id=question.assignment_id)
        section = crud.section.get_section_by_id(db=db, id=assignment.section_id)
        
        if current_user.role == "teacher":
            teacher = crud.user.get_teacher_by_user_id(db=db, id=current_user.user_id)
            if not teacher or section.teacher_id != teacher.teacher_id:
                raise HTTPException(
                    status_code=403,
                    detail="You don't have permission to view this question"
                )

        return question
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.put("/question/{question_id}", response_model=schemas.AssignmentQuestionInDB)
def update_question(
    *,
    db: Session = Depends(deps.get_db),
    question_id: UUID,
    question_in: schemas.AssignmentQuestionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Update a question.
    """
    question = crud.assignment_question.get_by_id(db=db, id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Verify teacher has access
    assignment = crud.assignment.get_by_id(db=db, id=question.assignment_id)
    section = crud.section.get_section_by_id(db=db, id=assignment.section_id)
    
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can update questions")

    teacher = crud.user.get_teacher_by_user_id(db=db, id=current_user.user_id)
    if not teacher or section.teacher_id != teacher.teacher_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to update this question"
        )

    return crud.assignment_question.update(db=db, db_obj=question, obj_in=question_in)

@router.delete("/question/{question_id}")
def delete_question(
    *,
    db: Session = Depends(deps.get_db),
    question_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Delete a question.
    """
    question = crud.assignment_question.get_by_id(db=db, id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Verify teacher has access
    assignment = crud.assignment.get_by_id(db=db, id=question.assignment_id)
    section = crud.section.get_section_by_id(db=db, id=assignment.section_id)
    
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can delete questions")

    teacher = crud.user.get_teacher_by_user_id(db=db, id=current_user.user_id)
    if not teacher or section.teacher_id != teacher.teacher_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete this question"
        )

    crud.assignment_question.delete(db=db, id=question_id)
    return {"message": "Question deleted successfully"}