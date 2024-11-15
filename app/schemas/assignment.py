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
    number_of_questions: int
    total_marks: str
    start_time: Optional[datetime] = None
    deadline: datetime

class AssignmentCreate(AssignmentBase):
    section_id: UUID
    assignment_materials : Optional[List[UUID]] = None
    questions : Optional[List[AssignmentQuestionCreate]] = None

class AssignmentUpdate(BaseModel):
    assignment_type: Optional[str] = None
    assignment_title: Optional[str] = None
    assignment_description: Optional[str] = None
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


# Add AssignmentMaterial schema
class AssignmentMaterialBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    library_item_id: UUID

class AssignmentMaterial(AssignmentMaterialBase):
    assignment_material_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
class Assignment(AssignmentInDBBase):
    assignment_questions: List[AssignmentQuestion] = []  # Changed from questions to assignment_questions
    assignment_materials: List[AssignmentMaterial] = []  # Changed to include full AssignmentMaterial objects

    class Config:
        from_attributes = True
        
        
