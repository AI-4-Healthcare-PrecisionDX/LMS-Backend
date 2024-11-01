# app/api/api_v1/endpoints/section.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models
from app.api import deps
from app.schemas.section import Section, SectionCreate, SectionUpdate

router = APIRouter()

@router.get("/", response_model=List[Section])
def get_sections(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve sections based on user role:
    - Teachers: Get their own sections
    - Admins: Get all sections
    """
    try:
        if current_user.role == "teacher":
            sections = crud.section.get_sections_by_teacher(
                db, user_id=current_user.user_id, skip=skip, limit=limit
            )
        elif current_user.role == "admin":
            sections = crud.section.get_multi(db, skip=skip, limit=limit)
        else:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to view sections"
            )
        return sections
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving sections: {str(e)}"
        )



@router.post("/create", response_model=Section)
def create_section(
    *,
    db: Session = Depends(deps.get_db),
    section_in: SectionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new section (Only for teachers).
    Section code will be automatically generated based on course name and sequence.
    Example: For a course named "Physics 101", sections might be "PHY101-01", "PHY101-02", etc.
    """
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can create sections"
        )

    # Verify course exists and teacher has access
    course = crud.template_course.get_course_by_id(db=db, id=section_in.template_course_id)
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # Check if teacher has access to the course
    has_access = crud.template_course.check_if_teacher_has_access(
        db=db, 
        template_course_id=section_in.template_course_id,
        user_id=current_user.user_id
    )
    if not has_access:
        raise HTTPException(
            status_code=403,
            detail="You don't have access to this course"
        )

    try:
        section = crud.section.create_section(
            db=db,
            obj_in=section_in,
            user_id=current_user.user_id
        )
        return section
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the section: {str(e)}"
        )

@router.put("/{section_id}", response_model=Section)
def update_section(
    *,
    db: Session = Depends(deps.get_db),
    section_id: UUID,
    section_in: SectionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a section (Only for teachers who own the section).
    Note: Section code cannot be updated as it is automatically generated.
    """
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can update sections"
        )

    section = crud.section.get_section_by_id(db=db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    # Check if the teacher owns the section
    if not crud.section.check_section_owner(
        db=db,
        section_id=section_id,
        teacher_id=current_user.user_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to update this section"
        )

    try:
        section = crud.section.update_section(
            db=db,
            db_obj=section,
            obj_in=section_in,
            teacher_id=current_user.user_id
        )
        return section
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating the section: {str(e)}"
        )

@router.get("/{section_id}", response_model=Section)
def get_section(
    *,
    db: Session = Depends(deps.get_db),
    section_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get section by ID.
    Teachers can only access their own sections.
    Admins can access any section.
    """
    section = crud.section.get_section_by_id(db=db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    if current_user.role == "teacher":
        # Check if the teacher owns the section
        if not crud.section.check_section_owner(
            db=db,
            section_id=section_id,
            teacher_id=current_user.user_id
        ):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this section"
            )
    elif current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access section details"
        )

    return section

@router.delete("/{section_id}")
def delete_section(
    *,
    db: Session = Depends(deps.get_db),
    section_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a section.
    Teachers can only delete their own sections.
    Admins can delete any section.
    """
    section = crud.section.get_section_by_id(db=db, id=section_id)
    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    if current_user.role == "teacher":
        # Check if the teacher owns the section
        if not crud.section.check_section_owner(
            db=db,
            section_id=section_id,
            teacher_id=current_user.user_id
        ):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this section"
            )
    elif current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete sections"
        )

    try:
        crud.section.delete_section(db=db, id=section_id)
        return {"message": "Section deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the section: {str(e)}"
        )