from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime




class AssignmentQuestionBase(BaseModel):
    question_type: Optional[str] = None
    question_text: Optional[str] = None
    question_answer: Optional[str] = None
    options_for_mcq: Optional[str] = None
    marks: Optional[str] = None
    question_description: Optional[str] = None
    
    
class AssignmentQuestionCreate(AssignmentQuestionBase):
    question_type: str
    question_text: str
    question_answer: str
    marks: str
    assignment_id: UUID
    

class AssignmentQuestionUpdate(AssignmentQuestionBase):
    pass

class AssignmentQuestionOut(AssignmentQuestionBase):
    question_id: UUID
    updated_at: datetime
    created_at: datetime
    assignment_id: UUID

    class Config:
        from_attributes = True
        
        
        

class AssignmentBase(BaseModel):
    assignment_type: Optional[str] = None
    assignment_title: Optional[str] = None
    assignment_description: Optional[str] = None
    assignment_question_type: Optional[str] = None
    number_of_questions: Optional[int] = None
    total_marks: Optional[str] = None
    start_time: Optional[datetime] = None
    deadline: Optional[datetime] = None

class AssignmentCreate(AssignmentBase):
    assignment_type: str
    assignment_title: str
    assignment_question_type: str
    number_of_questions: int
    total_marks: str
    start_time: datetime
    deadline: datetime
    section_id: UUID
    
class AssignmentUpdate(AssignmentBase):
    pass


class AssignmentOut(AssignmentBase):
    assignment_id: UUID
    updated_at: datetime
    created_at: datetime
    section_id: UUID
    questions : list[AssignmentQuestionOut]

    class Config:
        from_attributes = True
        
        
        
