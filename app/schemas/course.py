# app/schemas/course.py
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from .section import Section

class TemplateCourseBase(BaseModel):
    template_name: Optional[str] = None
    template_description: Optional[str] = None
    template_year: Optional[str] = None
    course_outline: Optional[str] = None
    department_id: Optional[UUID] = None

class TemplateCourseCreate(TemplateCourseBase):
    template_name: str
    department_id: UUID
    template_description: Optional[str] = None
    template_year: Optional[str] = None
    course_outline: Optional[str] = None
    template_course_access: Optional[List[UUID]] = None  # List of teacher IDs
    course_materials: Optional[List[UUID]] = None  # List of library_item_ids

class TemplateCourseUpdate(TemplateCourseBase):
    template_course_access: Optional[List[UUID]] = None
    course_materials: Optional[List[UUID]] = None

class TemplateCourseInDBBase(TemplateCourseBase):
    template_course_id: UUID
    admin_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TemplateCourse(TemplateCourseInDBBase):
    pass