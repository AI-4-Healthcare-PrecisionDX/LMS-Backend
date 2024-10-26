from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()



@router.get("/", response_model=List[schemas.AssignmentQuestionOut])
def get_questions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve questions.
    """
    # if current_user.role != "admin":
    #     raise HTTPException(
    #         status_code=403,
    #         detail="You do not have permission to perform this action",
    #     )
    questions = crud.assignment_question.get_multi(db, skip=skip, limit=limit)
    return questions

@router.get("/{id}", response_model=schemas.AssignmentQuestionOut)
def get_question_by_id(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve question by ID.
    """
    question = crud.assignment_question.get_question_by_id(db, id=id)
    if not question:
        raise HTTPException(
            status_code=404,
            detail="The question with this ID does not exist in the system",
        )
    return question



@router.post("/create-question", response_model=schemas.AssignmentQuestionOut)
def create_question(
    *,
    db: Session = Depends(deps.get_db),
    question_in: schemas.AssignmentQuestionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new question.
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
        
    print(f"Current user: {current_user}")
    
    try:
        admin = crud.assignment_question.get_admin_by_user_id(db, user_id=current_user.user_id)
    except Exception as e:
        print(f"Error retrieving admin: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the admin",
        )
        
    question = crud.assignment_question.create_question(db, obj_in=question_in, admin_id=admin.admin_id)
    return question


@router.put("/{id}", response_model=schemas.AssignmentQuestionOut)
def update_question(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    question_in: schemas.AssignmentQuestionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an question.
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
        
    question = crud.assignment_question.get_question_by_id(db, id=id)
    if not question:
        raise HTTPException(
            status_code=404,
            detail="The question with this ID does not exist in the system",
        )
    
    try:
        updated_question = crud.assignment_question.update_question(db, db_obj=question, obj_in=question_in, admin_id=current_user.user_id)
    except Exception as e:
        print(f"Error updating question: {str(e)}")
        
        
    return updated_question


@router.delete("/{id}", response_model=schemas.AssignmentQuestionOut)
def delete_question(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an question.
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
        
    question = crud.assignment_question.get_question_by_id(db, id=id)
    if not question:
        raise HTTPException(
            status_code=404,
            detail="The question with this ID does not exist in the system",
        )
    
    try:
        crud.assignment_question.delete_question(db, id=id)
    except Exception as e:
        print(f"Error deleting question: {str(e)}")
        
    return question



@router.get("/assignment", response_model=List[schemas.AssignmentOut])
def get_assignments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve assignments.
    """
    assignments = crud.assignment.get_multi(db, skip=skip, limit=limit)
    return assignments

@router.get("/assignment/{id}", response_model=schemas.AssignmentOut)
def get_assignment_by_id(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve assignment by ID.
    """
    assignment = crud.assignment.get_assignment_by_id(db, id=id)
    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="The assignment with this ID does not exist in the system",
        )
    return assignment

@router.post("/create-assignment", response_model=schemas.AssignmentOut)
def create_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_in: schemas.AssignmentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new assignment.
    """
    
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
        
    print(f"Current user: {current_user}")
    
    try:
        admin = crud.assignment.get_admin_by_user_id(db, user_id=current_user.user_id)
    except Exception as e:
        print(f"Error retrieving admin: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the admin",
        )
        
    assignment = crud.assignment.create_assignment(db, obj_in=assignment_in)
    return assignment


@router.put("/assignment/{id}", response_model=schemas.AssignmentOut)
def update_assignment(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    assignment_in: schemas.AssignmentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an assignment.
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
        
    assignment = crud.assignment.get_assignment_by_id(db, id=id)
    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="The assignment with this ID does not exist in the system",
        )
    
    try:
        updated_assignment = crud.assignment.update_assignment(db, db_obj=assignment, obj_in=assignment_in, admin_id=current_user.user_id)
    except Exception as e:
        print(f"Error updating assignment: {str(e)}")
        
        
    return updated_assignment


@router.delete("/assignment/{id}", response_model=schemas.AssignmentOut)
def delete_assignment(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an assignment.
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
        
    assignment = crud.assignment.get_assignment_by_id(db, id=id)
    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="The assignment with this ID does not exist in the system",
        )
    
    try:
        crud.assignment.delete_assignment(db, id=id)
    except Exception as e:
        print(f"Error deleting assignment: {str(e)}")
        
    return assignment


