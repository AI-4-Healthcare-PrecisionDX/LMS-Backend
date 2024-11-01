# app/schemas/assignment.py
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

# Assignment Question Schemas
class AssignmentQuestionBase(BaseModel):
    question_type: str
    question_text: str
    expected_answer: str
    options_for_mcq: Optional[List[str]] = None
    marks: int
    question_description: Optional[str] = None

class AssignmentQuestionCreate(AssignmentQuestionBase):
    pass

class AssignmentQuestionUpdate(BaseModel):
    question_type: Optional[str] = None
    question_text: Optional[str] = None
    expected_answer: Optional[str] = None
    options_for_mcq: Optional[List[str]] = None
    marks: Optional[int] = None
    question_description: Optional[str] = None

class AssignmentQuestionInDBBase(AssignmentQuestionBase):
    assignment_question_id: UUID
    assignment_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Assignment Schemas
class AssignmentBase(BaseModel):
    assignment_type: str  # traditional / ai generated
    assignment_title: str
    assignment_description: Optional[str] = None
    assignment_question_type: str
    number_of_questions: int
    total_marks: str
    start_time: Optional[datetime] = None
    deadline: datetime

class AssignmentCreate(AssignmentBase):
    section_id: UUID

class AssignmentUpdate(BaseModel):
    assignment_type: Optional[str] = None
    assignment_title: Optional[str] = None
    assignment_description: Optional[str] = None
    assignment_question_type: Optional[str] = None
    number_of_questions: Optional[int] = None
    total_marks: Optional[str] = None
    start_time: Optional[datetime] = None
    deadline: Optional[datetime] = None

class AssignmentInDBBase(AssignmentBase):
    assignment_id: UUID
    section_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Response Models
class AssignmentQuestion(AssignmentQuestionInDBBase):
    pass

class Assignment(AssignmentInDBBase):
    questions: List[AssignmentQuestion] = []