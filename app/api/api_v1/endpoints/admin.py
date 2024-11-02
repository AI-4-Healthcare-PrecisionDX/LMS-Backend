# app/api/api_v1/endpoints/admin.py

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


# Create admin user
@router.post("/create-admin/{branch_id}", response_model=schemas.Admin)
def create_admin(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreateAdmin,
    branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> schemas.Admin:
    """
    Create a new admin for a specific branch.
    """
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
        user = crud.user.create_admin_by_admin(db, obj_in=user_in, branch_id=branch_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user",
        )
    return user


# Create teacher user
@router.post("/create-teacher/{branch_id}", response_model=schemas.Teacher)
def create_teacher(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreateTeacher,
    branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> schemas.Teacher:
    """
    Create a new teacher for a specific branch.
    """
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
        user = crud.user.create_teacher_by_admin(
            db, obj_in=user_in, branch_id=branch_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user",
        )
    return user


@router.get("/teachers/{branch_id}", response_model=List[schemas.Teacher])
def get_teachers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve all teachers of a particular branch.
    """
    try:
        teachers = crud.user.get_all_teachers(
            db, skip=skip, limit=limit, branch_id=branch_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the teachers",
        )
    return teachers


@router.get(
    "/teachers/{branch_id}/teacher/{teacher_id}",
    response_model=schemas.user.UserInDBTeacher,
)
def get_teacher_by_id(
    teacher_id: UUID,
    db: Session = Depends(deps.get_db),
    branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve teacher by id.
    """
    try:
        teacher = crud.user.get_teacher_by_id(db, id=teacher_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the teacher",
        )
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@router.post("/create-student/{branch_id}", response_model=schemas.Student)
def create_student(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreateStudent,
    branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> schemas.Student:
    """
    Create a new student for a specific branch.
    """
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
        user = crud.user.create_student_by_admin(
            db, obj_in=user_in, branch_id=branch_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while creating the user",
        )
    return user


@router.get("/students/{branch_id}", response_model=List[schemas.Student])
def get_students(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve all students of a particular branch.
    """
    try:
        students = crud.user.get_all_students(
            db, skip=skip, limit=limit, branch_id=branch_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the students",
        )
    return students


@router.get(
    "/students/{branch_id}/student/{student_id}", response_model=schemas.Student
)
def get_student_by_id(
    student_id: UUID,
    db: Session = Depends(deps.get_db),
    branch_id: UUID = Depends(deps.check_branch),
    current_user: models.user.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Retrieve student by id.
    """
    try:
        student = crud.user.get_student_by_id(db, id=student_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the student",
        )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
