# app/api/api_v1/endpoints/course.py
from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models, schemas
from app.api import deps
from app.schemas.course import (
    TemplateCourse,
    TemplateCourseCreate,
    TemplateCourseUpdate,
)

router = APIRouter()

@router.get("/", response_model=List[TemplateCourse])
def get_courses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all template courses.
    """
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    courses = crud.template_course.get_multi(db, skip=skip, limit=limit)
    return courses

@router.get("/department/{department_id}", response_model=List[TemplateCourse])
def get_department_courses(
    department_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all courses in a specific department.
    """
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    return crud.template_course.get_courses_by_department(
        db=db, department_id=department_id
    )

@router.get("/{course_id}", response_model=TemplateCourse)
def get_course(
    course_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific course by ID.
    """
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    course = crud.template_course.get_course_by_id(db=db, id=course_id)
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    return course

@router.post("/", response_model=TemplateCourse)
def create_course(
    *,
    db: Session = Depends(deps.get_db),
    course_in: TemplateCourseCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new template course.
    First creates the base course, then adds materials and access if provided.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can create courses"
        )
        
    try:
        # Get admin record
        admin = crud.template_course.get_admin_by_user_id(db=db, user_id=current_user.user_id)
        if not admin:
            raise HTTPException(
                status_code=404,
                detail="Admin not found"
            )
        
        # Create base course first
        course = crud.template_course.create_base_course(
            db=db,
            obj_in=course_in,
            admin_id=admin.admin_id
        )
        
        # Add teacher access if provided
        if course_in.template_course_access:
            crud.template_course.add_course_access(
                db=db,
                template_course_id=course.template_course_id,
                teacher_ids=course_in.template_course_access
            )
        
        # Add course materials if provided
        if course_in.course_materials:
            crud.template_course.add_course_materials(
                db=db,
                template_course_id=course.template_course_id,
                library_item_ids=course_in.course_materials,
                user_id=current_user.user_id
            )
            
        # Refresh the course to get the updated relationships
        db.refresh(course)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
    return course

@router.put("/{course_id}", response_model=TemplateCourse)
def update_course(
    *,
    db: Session = Depends(deps.get_db),
    course_id: UUID,
    course_in: TemplateCourseUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a template course.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can update courses"
        )
        
    course = crud.template_course.get_course_by_id(db=db, id=course_id)
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
        
    try:
        admin = crud.template_course.get_admin_by_user_id(db=db, user_id=current_user.user_id)
        if not admin:
            raise HTTPException(
                status_code=404,
                detail="Admin not found"
            )
            
        course = crud.template_course.update_course(
            db=db,
            db_obj=course,
            obj_in=course_in,
            user_id=current_user.user_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    return course

@router.delete("/{course_id}")
def delete_course(
    *,
    db: Session = Depends(deps.get_db),
    course_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a template course and all associated records.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can delete courses"
        )
        
    try:
        crud.template_course.delete_course(db=db, id=course_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    return {"message": "Course and associated records deleted successfully"}