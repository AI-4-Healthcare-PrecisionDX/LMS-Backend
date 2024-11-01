# app/schemas/section.py
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from .course import TemplateCourse

# Modify TeacherInfo to include user info
class TeacherInfo(BaseModel):
    teacher_id: UUID
    user_id: UUID
    user: Optional["UserBase"] = None  # Will contain user details including name
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True

    @property
    def name(self) -> str:
        """Return full name or email if name not available"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    class Config:
        from_attributes = True

# Update TeacherInfo to include UserBase
TeacherInfo.model_rebuild()

class SectionBase(BaseModel):
    section_name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    template_course_id: Optional[UUID] = None

class SectionCreate(BaseModel):
    section_name: str
    start_date: datetime
    end_date: datetime
    template_course_id: UUID

class SectionUpdate(BaseModel):
    section_name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    template_course_id: Optional[UUID] = None

class SectionInDBBase(SectionBase):
    section_id: UUID
    section_code: str  # Read-only, automatically generated
    teacher_id: UUID
    template_course_id: UUID
    created_at: datetime
    updated_at: datetime
    teacher: Optional[TeacherInfo] = None
    template_course: Optional[TemplateCourse] = None
    student_count: Optional[int] = None

    class Config:
        from_attributes = True

class Section(SectionInDBBase):
    pass

class SectionInDB(SectionInDBBase):
    pass