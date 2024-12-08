from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.combined import SectionCombinedResponse
from app.crud.crud_combined import get_section_combined_data
from app.api import deps
from app import crud, models

router = APIRouter()

@router.get("/section_updates/{section_id}", response_model=SectionCombinedResponse)
def get_combined_section_data(
    section_id: UUID,
    current_student: models.User = Depends(deps.get_current_active_student_user),
    db: Session = Depends(deps.get_db),
):
    # Fetch data
    result = get_section_combined_data(db=db, section_id=section_id, student_id=current_student.student_id)
    
    if not result:
        raise HTTPException(status_code=403, detail="Student isn't a member of this section or Section data not found")

    return result