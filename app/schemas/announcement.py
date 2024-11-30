from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from .section import SectionBase, TeacherInfo

# First, let's create a minimal section info class for announcements
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
    section_id: UUID
    teacher_id: UUID
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

# You might also want a more detailed response model
class AnnouncementWithDetails(AnnouncementInDB):
    """
    A more detailed announcement model that includes full section and teacher information
    """
    class Config:
        from_attributes = True