#app/api/api_v1/endpoints/admin.py

from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from uuid import UUID

router = APIRouter()


# Admin can create a new user.
# Assign the role of the user to be (admin, teacher, student).
# Admin can create a new library, template_course.

@router.post("/create-teacher", response_model=schemas.user.UserInDBTeacher)
def create_teacher(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreateTeacher,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user.
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
    # Check if the user already exists
    try:
        user = crud.user.get_by_email(db, email=user_in.email)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the user",
        )

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )

    try:
        user = crud.user.create_teacher(db, obj_in=user_in)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user",
        )

    return user


@router.get("/teachers", response_model=List[schemas.user.UserInDBTeacher])
def get_teachers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all teachers.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
    teachers = crud.user.get_all_teachers(db, skip=skip, limit=limit)
    return teachers

@router.get("/teacher/{teacher_id}", response_model=schemas.user.UserInDBTeacher)
def get_teacher_by_id(
    teacher_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve teacher by id.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
    teacher = crud.user.get_teacher_by_id(db, id=teacher_id)  # Changed parameter name to match crud method
    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )
    return teacher

@router.get("/students", response_model=List[schemas.user.UserInDBStudent])
def get_students(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all students.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
    students = crud.user.get_all_students(db, skip=skip, limit=limit)
    return students

@router.get("/student/{student_id}", response_model=schemas.user.UserInDBStudent)
def get_student_by_id(
    student_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve student by id.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
    student = crud.user.get_student_by_id(db, id=student_id)  # Changed parameter name to match crud method
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return student



@router.post("/create-student", response_model=schemas.user.UserInDBStudent)
def create_student(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreateStudent,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new user.
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
    # Check if the user already exists
    try:
        user = crud.user.get_by_email(db, email=user_in.email)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the user",
        )

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )

    try:
        user = crud.user.create_student(db, obj_in=user_in)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user",
        )

    return user