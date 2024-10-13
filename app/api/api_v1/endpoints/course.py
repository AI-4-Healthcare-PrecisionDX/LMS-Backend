from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.TemplateCourse])
def get_courses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve courses.
    """
    # if current_user.role != "admin":
    #     raise HTTPException(
    #         status_code=403,
    #         detail="You do not have permission to perform this action",
    #     )
    courses = crud.course.get_multi(db, skip=skip, limit=limit)
    return courses


@router.post("/create-course", response_model=schemas.TemplateCourse)
def create_course(
    *,
    db: Session = Depends(deps.get_db),
    course_in: schemas.TemplateCourseCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new course.
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
        
    print(f"Current user: {current_user}")
    
    try:
        admin = crud.course.get_admin_by_user_id(db, user_id=current_user.user_id)
    except Exception as e:
        print(f"Error retrieving admin: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the admin",
        )
        
        
    try:
        course = crud.course.create_course(db, obj_in=course_in, admin_id=admin.admin_id)
    except Exception as e:
        print(f"Error creating course: {str(e)}")  # Log the specific error
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the course: {str(e)}",
        )
    return course

@router.put("/update-course/{course_id}", response_model=schemas.TemplateCourse)
def update_course(
    *,
    db: Session = Depends(deps.get_db),
    course_id: str,
    course_in: schemas.TemplateCourseUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a course.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
    
    course = crud.course.get_course_by_id(db, id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    try:
        admin = crud.course.get_admin_by_user_id(db, user_id=current_user.user_id)
        if admin is None:
            raise HTTPException(status_code=404, detail="Admin not found")
    except Exception as e:
        print(f"Error retrieving admin: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the admin",
        )
        
    try:
        updated_course = crud.course.update_course(db, db_obj=course, obj_in=course_in, admin_id=admin.admin_id)
    except Exception as e:
        print(f"Error updating course: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating the course: {str(e)}",
        )
    return updated_course

@router.get("/get-course/{course_id}", response_model=schemas.TemplateCourse)
def read_course(
    course_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific course by ID.
    """
    course = crud.course.get_course_by_id(db, id=course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.delete("/delete-course/{course_id}")
def delete_course(
    course_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a course.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this action",
        )
    try:
        crud.course.delete_course(db, id=course_id)
    except Exception as e:
        print(f"Error deleting course: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the course: {str(e)}",
        )
    return {"message": "Course deleted successfully"}