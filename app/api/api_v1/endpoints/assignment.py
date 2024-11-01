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
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Create new assignment.
    """
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can create assignments"
        )

    # Verify section exists and teacher has access
    section = crud.section.get_section_by_id(db=db, id=assignment_in.section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    teacher = crud.user.get_teacher_by_user_id(db=db, id=current_user.user_id)
    if not teacher or section.teacher_id != teacher.teacher_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to create assignments in this section"
        )

    try:
        return crud.assignment.create(db=db, obj_in=assignment_in)
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
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Update an assignment.
    """
    assignment = crud.assignment.get_by_id(db=db, id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Verify teacher has access
    section = crud.section.get_section_by_id(db=db, id=assignment.section_id)
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can update assignments")

    teacher = crud.user.get_teacher_by_user_id(db=db, id=current_user.user_id)
    if not teacher or section.teacher_id != teacher.teacher_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to update this assignment"
        )

    try:
        return crud.assignment.update(db=db, db_obj=assignment, obj_in=assignment_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{assignment_id}")
def delete_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Delete an assignment.
    """
    assignment = crud.assignment.get_by_id(db=db, id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Verify teacher has access
    section = crud.section.get_section_by_id(db=db, id=assignment.section_id)
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can delete assignments")

    teacher = crud.user.get_teacher_by_user_id(db=db, id=current_user.user_id)
    if not teacher or section.teacher_id != teacher.teacher_id:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete this assignment"
        )

    crud.assignment.delete(db=db, id=assignment_id)
    return {"message": "Assignment deleted successfully"}

# Assignment Questions Endpoints
@router.post("/{assignment_id}/questions", response_model=schemas.AssignmentQuestion)
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

@router.post("/{assignment_id}/questions/batch", response_model=List[schemas.AssignmentQuestion])
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

@router.get("/question/{question_id}", response_model=schemas.AssignmentQuestion)
def read_question(
    question_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get question by ID.
    """
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

@router.put("/question/{question_id}", response_model=schemas.AssignmentQuestion)
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