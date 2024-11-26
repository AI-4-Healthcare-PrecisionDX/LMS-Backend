# app/schemas/section.py
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from .course import TemplateCourse
from .library import Library

class TeacherInfo(BaseModel):
    teacher_id: UUID
    user_id: UUID
    user: Optional["UserBase"] = None

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True

    @property
    def name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    class Config:
        from_attributes = True

TeacherInfo.model_rebuild()

class SectionExclusiveContentBase(BaseModel):
    section_id: UUID
    library_item_id: UUID

class SectionExclusiveContentCreate(SectionExclusiveContentBase):
    title : Optional[str] = None
    description: Optional[str] = None
    pass

class SectionExclusiveContentInDB(SectionExclusiveContentBase):
    title : Optional[str] = None
    description: Optional[str] = None
    section_exclusive_content_id: UUID
    user_id: UUID
    library_item: Optional[Library] = None

    class Config:
        from_attributes = True
        
class SectionExclusiveContentByCourseTeacher(BaseModel):
    course_id: UUID
    library_item_id: UUID
    
class SectionExclusiveContentByCourseTeacherCreate(SectionExclusiveContentByCourseTeacher):
    title : Optional[str] = None
    description: Optional[str] = None
    pass

class SectionExclusiveContentByCourseTeacherInDB(SectionExclusiveContentByCourseTeacher):
    title : Optional[str] = None
    description: Optional[str] = None
    section_exclusive_content_id: UUID
    user_id: UUID
    library_item: Optional[Library] = None

    class Config:
        from_attributes = True

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
    teacher_id: UUID

class SectionUpdate(BaseModel):
    section_name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    template_course_id: Optional[UUID] = None
    teacher_id: Optional[UUID] = None

class SectionInDBBase(SectionBase):
    section_id: UUID
    section_code: str
    teacher_id: UUID
    template_course_id: UUID
    created_at: datetime
    updated_at: datetime
    teacher: Optional[TeacherInfo] = None
    template_course: Optional[TemplateCourse] = None
    student_count: Optional[int] = None
    section_exclusive_contents: List[SectionExclusiveContentInDB] = []

    class Config:
        from_attributes = True

class Section(SectionInDBBase):
    pass