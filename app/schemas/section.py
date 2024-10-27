#app/schemas/section.py

from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


# Shared properties for section
class SectionBase(BaseModel):
    section_name: Optional[str] = None
    section_code: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    template_course_id: Optional[UUID] = None

# Properties to receive on section creation
class SectionCreate(SectionBase):
    section_name: str
    section_code: str
    start_date: datetime
    end_date: datetime
    template_course_id: UUID

# Properties to receive on section update
class SectionUpdate(SectionBase):
    template_course_id: UUID
    pass

# Base class for properties stored in the DB
class SectionInDBBase(SectionBase):
    section_id: Optional[UUID] = None
    teacher_id: UUID
    template_course_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Use this for correct ORM mapping

# Properties to return to the client
class Section(SectionInDBBase):
    pass

# Properties stored in DB
class SectionInDB(SectionInDBBase):
    pass
