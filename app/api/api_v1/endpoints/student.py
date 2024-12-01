from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models
from app.api import deps
from app.schemas.section import (
    Section,

) 

router = APIRouter()


@router.post("/join-section", response_model=Section)
def join_section(
    *,
    db: Session = Depends(deps.get_db),
    section_code: str,
    current_student: models.User = Depends(deps.get_current_active_student_user),
) -> Any:
    """
    Join a section (Only for authorized users).
    """

    try:
        section = crud.section.join_section(
            db, section_code=section_code, student_id=current_student.student_id
        )
        return section
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/get-sections", response_model=List[Section])
def get_sections(
    db: Session = Depends(deps.get_db),
    current_student: models.User = Depends(deps.get_current_active_student_user),
) -> Any:
    
    
    try:
        sections = crud.section.get_sections_for_student(db, student_id=current_student.student_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return sections
