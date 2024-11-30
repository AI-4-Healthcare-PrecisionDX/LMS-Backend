from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from .section import SectionBase, TeacherInfo


class SectionInfo(BaseModel):
    section_id: UUID
    section_name: str
    section_code: str

    class Config:
        from_attributes = True

class AnnouncementBase(BaseModel):
    announcement_title: str
    announcement_description: Optional[str] = None

    
class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    announcement_title: Optional[str] = None
    announcement_description: Optional[str] = None
    
class AnnouncementInDB(AnnouncementBase):
    announcement_id: UUID
    created_at: datetime
    updated_at: datetime
    section: Optional[SectionInfo] = None
    teacher: Optional[TeacherInfo] = None

    class Config:
        from_attributes = True

class Announcement(AnnouncementInDB):

    class Config:
        from_attributes = True