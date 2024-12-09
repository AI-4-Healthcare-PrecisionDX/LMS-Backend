from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models
from app.api import deps
from app.schemas.section import (
    Section as SectionSchema,
    SectionCreate,
    SectionUpdate,
    SectionExclusiveContentCreate,
    SectionExclusiveContentInDB
)

router = APIRouter()

@router.get("/", response_model=List[SectionSchema])
def get_sections(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """Get all sections (admin only)"""

    try:
        sections = crud.section.get_multi(db, skip=skip, limit=limit, branch_id=current_user.branch_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving sections: {str(e)}"
        )
        
    #filter the sections that  
    return sections

@router.get("/teacher", response_model=List[SectionSchema])
def get_teacher_sections(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user),
) -> Any:
    """Get all sections for the current teacher"""

    try:
        sections = crud.section.get_sections_by_teacher(
        db=db, teacher_id=current_teacher.teacher_id, skip=skip, limit=limit
    )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving sections: {str(e)}"
        )
        
    return sections

@router.post("/create", response_model=SectionSchema)
def create_section(
    *,
    db: Session = Depends(deps.get_db),
    section_in: SectionCreate,
    current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:


    # Verify course exists
    try:
        course = crud.template_course.get_course_by_id(db=db, id=section_in.template_course_id)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while verifying the course: {str(e)}"
        )
    
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
            
    # verify teacher exists
    try:
        teacher = crud.user.get_teacher_by_id(db=db, id=section_in.teacher_id)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while verifying the teacher: {str(e)}"
        )
    
    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )


    try:
        section = crud.section.create_section(
            db=db,
            obj_in=section_in,
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

@router.put("/{section_id}", response_model=SectionSchema)
def update_section(
    *,
    db: Session = Depends(deps.get_db),
    section_id: UUID,
    section_in: SectionUpdate,
    current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:
    """
    Update a section (Only for teachers who own the section).
    Note: Section code cannot be updated as it is automatically generated.
    """

    try:
        section = crud.section.get_section_by_id(db=db, id=section_id)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving the section: {str(e)}"
        )
        
    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    try:
        section = crud.section.update_section(
            db=db,
            db_obj=section,
            obj_in=section_in
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

@router.get("/{section_id}", response_model=SectionSchema)
def get_section(
    *,
    db: Session = Depends(deps.get_db),
    section_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    try:
        section = crud.section.get_section_by_id(db=db, id=section_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving the section: {str(e)}"
        )
        
    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )
    
    if current_user.role == "admin":
        return section
        
    try:
        teacher = crud.user.get_teacher_by_user_id(db=db, id=current_user.user_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while verifying the teacher: {str(e)}"
        )

    if current_user.role == "teacher" or current_user.role == "admin":
        # Check if the teacher owns the section
        if not crud.section.check_section_owner(
            db=db,
            section_id=section_id,
            teacher_id=teacher.teacher_id
        ):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this section"
            )
    else:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this section"
        )
        

    return section

@router.delete("/{section_id}")
def delete_section(
    *,
    db: Session = Depends(deps.get_db),
    section_id: UUID,
    current_user: models.User = Depends(deps.get_current_active_admin_user),
) -> Any:


        
    try:
        section = crud.section.get_section_by_id(db=db, id=section_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving the section: {str(e)}"
        )
        
    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    try:
        crud.section.delete_section(db=db, id=section_id)
        return {"message": "Section deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the section: {str(e)}"
        )

@router.get(
    "/{section_id}/contents",
    response_model=List[SectionExclusiveContentInDB]
)
def get_section_contents(
    section_id: UUID,
    db: Session = Depends(deps.get_db),
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:

    # First check if section exists
    try:
        section = crud.section.get_section_by_id(db=db, id=section_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving the section: {str(e)}"
        )
        
    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    # Check permissions
    if not crud.section.check_section_owner(
        db=db,
        section_id=section_id,
        teacher_id=current_teacher.teacher_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to access this section"
        )

    try:
        contents = crud.section.get_section_contents(
            db=db,
            section_id=section_id,
            skip=skip,
            limit=limit
        )
        return contents
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving section contents: {str(e)}"
        )

@router.post("/{section_id}/content", response_model=SectionExclusiveContentInDB)
def add_section_content(
    *,
    db: Session = Depends(deps.get_db),
    content: SectionExclusiveContentCreate,
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user),
) -> Any:
    """
    Add exclusive content to a section.
    Only teachers who own the section or admins can add content.
    """
    try:
        section = crud.section.get_section_by_id(db=db, id=content.section_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving the section: {str(e)}"
        )
        
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    if not crud.section.check_section_owner(
        db=db,
        section_id=content.section_id,
        teacher_id=current_teacher.teacher_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to add content to this section"
        )

    # Check if library item exists
    try:
        library_item = crud.library.get_by_uuid(db=db, library_id=content.library_item_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving the library item: {str(e)}"
        )
        
    if not library_item:
        raise HTTPException(status_code=404, detail="Library item not found")

    try:
        return crud.section.add_exclusive_content(
            db=db,
            user_id=current_teacher.user_id,
            content_in=content
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while adding content to section: {str(e)}"
        )

@router.delete("/{section_id}/content/{section_exclusive_content_id}", response_model=dict)
def remove_section_content(
    *,
    db: Session = Depends(deps.get_db),
    section_id: UUID,
    section_exclusive_content_id: UUID,
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user),
) -> Any:
    """
    Remove exclusive content from a section.
    Only teachers who own the section or admins can remove content.
    """
    try:
        section = crud.section.get_section_by_id(db=db, id=section_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving the section: {str(e)}"
        )
        
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    if not crud.section.check_section_owner(
        db=db,
        section_id=section_id,
        teacher_id=current_teacher.teacher_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to remove content from this section"
        )
        

    try:
        success = crud.section.remove_exclusive_content(
            db=db,
            section_id=section_id,
            section_exclusive_content_id=section_exclusive_content_id
        )
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Content not found in this section"
            )
        return {"message": "Content removed from section successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while removing content from section: {str(e)}"
        )
        
        
        