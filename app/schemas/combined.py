from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from .course import TemplateCourse


class DepartmentBase(BaseModel):
    department_name: str
    department_id: UUID
    branch_id: UUID
    updated_at: datetime

    class Config:
        from_attributes = True


# class TemplateCourseBase(BaseModel):
#     template_course_id: UUID
#     template_name: str
#     template_description: str
#     template_year: str
#     course_outline: str
#     department_id: UUID
#     admin_id: UUID
#     created_at: datetime
#     updated_at: datetime
#     course_materials: List[dict]
#     branch_id: UUID
#     department: DepartmentBase

#     class Config:
#         from_attributes = True



class AnnouncementBase(BaseModel):
    announcement_id: UUID
    announcement_title: str
    announcement_description: Optional[str]
    section_id: UUID
    teacher_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SectionExclusiveContentBase(BaseModel):
    section_exclusive_content_id: UUID
    title: Optional[str]
    description: Optional[str]
    user_id: UUID
    section_id: UUID
    library_item_id: UUID

    class Config:
        from_attributes = True

class AssignmentBase(BaseModel):
    assignment_id: UUID
    assignment_type: str
    assignment_title: str
    assignment_description: Optional[str]
    number_of_questions: int
    total_marks: int
    start_time: Optional[datetime]
    deadline: datetime
    created_at: datetime
    updated_at: datetime
    section_id: UUID

    class Config:
        from_attributes = True

class AssignmentQuestionBase(BaseModel):
    assignment_question_id: UUID
    question_type: Optional[str]
    question_text: str
    options_for_mcq: Optional[List[str]] = None
    marks: int
    question_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AssignmentMaterialBase(BaseModel):
    assignment_material_id: UUID
    title: Optional[str]
    description: Optional[str]
    library_item_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AssignmentWithDetails(AssignmentBase):
    assignment_questions: List[AssignmentQuestionBase] = []
    assignment_materials: List[AssignmentMaterialBase] = []

class SectionCombinedResponse(BaseModel):
    template_course: TemplateCourse
    announcements: List[AnnouncementBase]
    section_exclusive_contents: List[SectionExclusiveContentBase]
    assignments: List[AssignmentWithDetails]
    
    class Config:
        from_attributes = True
