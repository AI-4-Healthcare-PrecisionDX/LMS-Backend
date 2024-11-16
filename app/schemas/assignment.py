# app/schemas/assignment.py
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Dict, Any

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

class AssignmentQuestionInDB(AssignmentQuestionBase):
    assignment_question_id: UUID
    assignment_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Assignment Material Schema
class AssignmentMaterialBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    library_item_id: UUID

class AssignmentMaterialInDB(AssignmentMaterialBase):
    assignment_material_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Assignment Schemas
class AssignmentBase(BaseModel):
    assignment_type: str
    assignment_title: str
    assignment_description: Optional[str] = None
    number_of_questions: int
    total_marks: int
    start_time: Optional[datetime] = None
    deadline: datetime

class AssignmentCreate(AssignmentBase):
    section_id: UUID
    assignment_materials: Optional[List[UUID]] = None
    questions: Optional[List[AssignmentQuestionCreate]] = None

class AssignmentUpdate(BaseModel):
    assignment_type: Optional[str] = None
    assignment_title: Optional[str] = None
    assignment_description: Optional[str] = None
    number_of_questions: Optional[int] = None
    total_marks: Optional[int] = None
    start_time: Optional[datetime] = None
    deadline: Optional[datetime] = None
    assignment_materials: Optional[List[UUID]] = None
    questions: Optional[List[AssignmentQuestionCreate]] = None

# Response Models
class Assignment(AssignmentBase):
    assignment_id: UUID
    section_id: UUID
    created_at: datetime
    updated_at: datetime
    assignment_questions: List[AssignmentQuestionInDB] = []
    assignment_materials: List[AssignmentMaterialInDB] = []
    
    model_config = ConfigDict(from_attributes=True)
    
    
class DeleteAssignmentResponse(BaseModel):
    message: str
    details: Dict[str, Any]