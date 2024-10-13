from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime
from .super_admin import Department


class TemplateCourseBase(BaseModel):
    template_name: Optional[str] = None
    template_description: Optional[str] = None
    template_year: Optional[str] = None
    course_outline: Optional[str] = None
    
class TemplateCourseCreate(TemplateCourseBase):
    template_name: str
    department_id: UUID

class TemplateCourseUpdate(TemplateCourseBase):
    department_id: UUID
    pass

class TemplateCourseInDBBase(TemplateCourseBase):
    template_course_id: Optional[UUID] = None
    admin_id: UUID
    department_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
class TemplateCourse(TemplateCourseInDBBase):
    department_id: UUID
    department : Department
    pass

class TemplateCourseInDB(TemplateCourseInDBBase):
    pass


