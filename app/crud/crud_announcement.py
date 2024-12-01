# app/crud/crud_course.py
from typing import Any, Dict, Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from app.crud.base import CRUDBase
from app.models.announcement import Announcement
from app.models.admin import Admin
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate
from app.models.teacher import Teacher
from app.models.section import Section
from fastapi import HTTPException
from uuid import UUID

class CRUDAnnouncement(CRUDBase[Announcement, AnnouncementCreate, AnnouncementUpdate]):
    def get_all_announcements_for_teacher(self, db: Session,*, skip: int = 0, limit: int = 100, teacher_id: UUID):
        try:
            return db.query(Announcement).filter(Announcement.teacher_id == teacher_id).offset(skip).limit(limit).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def get_all_announcements_for_section(self,db: Session,*, skip: int = 0, limit: int = 100, teacher_id: UUID, section_id: UUID):
        try:
            return db.query(Announcement).filter(Announcement.teacher_id == teacher_id, Announcement.section_id == section_id).offset(skip).limit(limit).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def create_announcement(self, db: Session, *, announcement_in: AnnouncementCreate, section_id: UUID, teacher_id: UUID):
        try:
            announcement = Announcement(**announcement_in.dict(), teacher_id=teacher_id, section_id=section_id)
            db.add(announcement)
            db.commit()
            db.refresh(announcement)
            return announcement
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def get_announcement_by_id(self, db: Session, *, announcement_id: UUID):
        try:
            return db.query(Announcement).filter(Announcement.announcement_id == announcement_id).first()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        
    def update_announcement(self, db: Session, *, announcement: Announcement, announcement_in: AnnouncementUpdate):
        try:
            for key, value in announcement_in.dict().items():
                setattr(announcement, key, value)
            db.add(announcement)
            db.commit()
            db.refresh(announcement)
            return announcement
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    def delete_announcement(self, db: Session, *, announcement_id: UUID, teacher_id: UUID):
        try:
            db.query(Announcement).filter(Announcement.announcement_id == announcement_id, Announcement.teacher_id == teacher_id).delete()
            db.commit()
            return announcement
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    
announcement = CRUDAnnouncement(Announcement)