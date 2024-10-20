from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models
from app.api import deps
from app.schemas.section import Section, SectionCreate, SectionUpdate  # Correct schema imports

router = APIRouter()


@router.get("/", response_model=List[Section])
def get_sections(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all sections.
    """
    sections = crud.section.get_multi(db, skip=skip, limit=limit)
    return sections


@router.post("/create-section", response_model=Section)
def create_section(
    *,
    db: Session = Depends(deps.get_db),
    section_in: SectionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new section (Only for teachers).
    """
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can create sections",
        )

    try:
        section = crud.section.create_section(db, obj_in=section_in, teacher_id=current_user.user_id)
    except Exception as e:
        print(f"Error creating section: {str(e)}")  # Log the specific error
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the section: {str(e)}",
        )
    return section


@router.put("/update-section/{section_id}", response_model=Section)
def update_section(
    *,
    db: Session = Depends(deps.get_db),
    section_id: UUID,
    section_in: SectionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a section (Only for teachers).
    """
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can update sections",
        )

    section = crud.section.get_section_by_id(db=db, id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    try:
        updated_section = crud.section.update_section(db, db_obj=section, obj_in=section_in, teacher_id=current_user.user_id)
    except Exception as e:
        print(f"Error updating section: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating the section: {str(e)}",
        )
    return updated_section


@router.get("/get-section/{section_id}", response_model=Section)
def read_section(
    section_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific section by ID.
    """
    section = crud.section.get_section_by_id(db=db, id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


@router.delete("/delete-section/{section_id}")
def delete_section(
    section_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a section (Only for teachers).
    """
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="Only teachers can delete sections",
        )
    
    section = crud.section.get_section_by_id(db=db, id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    try:
        crud.section.delete_section(db, id=section_id)
    except Exception as e:
        print(f"Error deleting section: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the section: {str(e)}",
        )
    return {"message": "Section deleted successfully"}
