from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models
from app.api import deps
from app.schemas.announcement import Announcement, AnnouncementCreate, AnnouncementUpdate

router = APIRouter()



@router.get("/", response_model=List[Announcement])
def get_announcements(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user),
) -> Any:
    """
    Retrieve all announcements.
    """
    
    try:
        announcements = crud.announcement.get_all_announcements_for_teacher(db, skip=skip, limit=limit, teacher_id=current_teacher.teacher_id)
        return announcements
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
    
    
#get announcement for individual section
@router.get("/section/{section_id}", response_model=List[Announcement])
def get_announcements_for_section(
    section_id: UUID,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user),
) -> Any:
    """
    Get all announcements for a specific section.
    """
    try:
        announcements = crud.announcement.get_all_announcements_for_section(db,skip=skip, limit=limit, teacher_id=current_teacher.teacher_id, section_id=section_id)
        return announcements
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
    
@router.post("/{section_id}", response_model=Announcement)
def create_announcement(
    *,
    db: Session = Depends(deps.get_db),
    section_id: UUID,
    announcement_in: AnnouncementCreate,
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user),
) -> Any:
    """
    Create new announcement.
    """
    try:
        announcement = crud.announcement.create_announcement(db=db, announcement_in=announcement_in, teacher_id=current_teacher.teacher_id, section_id=section_id)
        return announcement
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
    
@router.put("/{announcement_id}", response_model=Announcement)
def update_announcement(
    *,
    db: Session = Depends(deps.get_db),
    announcement_id: UUID,
    announcement_in: AnnouncementUpdate,
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user),
) -> Any:
    """
    Update an announcement.
    """
    try:
        announcement = crud.announcement.get_announcement_by_id(db=db, announcement_id=announcement_id)
        if not announcement:
            raise HTTPException(status_code=404, detail="Announcement not found")
        if announcement.teacher_id != current_teacher.teacher_id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        announcement = crud.announcement.update_announcement(db=db, announcement=announcement, announcement_in=announcement_in)
        return announcement
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
    
@router.delete("/{announcement_id}", response_model=dict)
def delete_announcement(
    *,
    db: Session = Depends(deps.get_db),
    announcement_id: UUID,
    current_teacher: models.User = Depends(deps.get_current_active_teacher_user),
) -> Any:
    """
    Delete an announcement.
    """

    try:
        crud.announcement.delete_announcement(db=db, announcement_id=announcement_id, teacher_id=current_teacher.teacher_id)
        return {"message": "Announcement deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))