from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID  # Import UUID type
from app.schemas.combined import SectionCombinedResponse
from app.crud.crud_combined import get_section_combined_data
from app.api import deps

router = APIRouter()

@router.get("/section_updates/{section_id}", response_model=SectionCombinedResponse)
def get_combined_section_data(
    section_id: UUID,  # Change section_id to UUID
    db: Session = Depends(deps.get_db),
):
    # Fetch data
    result = get_section_combined_data(db=db, section_id=section_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Section data not found")

    return SectionCombinedResponse(
        announcements=result["announcements"],
        section_exclusive_contents=result["section_exclusive_contents"],
        assignments=result["assignments"],
    )
