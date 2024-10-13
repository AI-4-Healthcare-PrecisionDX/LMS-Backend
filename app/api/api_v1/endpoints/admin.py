from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

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