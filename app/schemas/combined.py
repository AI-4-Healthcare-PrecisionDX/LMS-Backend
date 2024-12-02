# app/schemas/combined.py
# This is combined version of Announcement, SectionExclusiveContent and Assignment schemas

from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

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

class SectionCombinedResponse(BaseModel):
    announcements: List[AnnouncementBase]
    section_exclusive_contents: List[SectionExclusiveContentBase]
    assignments: List[AssignmentBase]
