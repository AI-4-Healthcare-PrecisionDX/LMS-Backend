# app/schemas/assignment.py
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Dict, Any
from .assignment import AssignmentQuestionInDB


# Assignment Question Schemas
class AssignmentSubmissionBase(BaseModel):
    total_marks_after_eval : Optional[int] = None
    evaluated : Optional[bool] = None
    
    
class AssignmentSubmissionCreate(AssignmentSubmissionBase):
    assignment_id: UUID
    student_id: UUID
    pass

class AssignmentSubmissionUpdate(AssignmentSubmissionBase):
    pass
    
class AssignmentSubmissionAnswerBase(BaseModel):
    answers : List[str]= None
    total_marks_after_eval : Optional[int] = None
    
class AssignmentSubmissionAnswerCreate(AssignmentSubmissionAnswerBase):
    assignment_submission_id: UUID
    question_id: UUID
    student_id: UUID
    pass

class AssignmentSubmissionAnswerUpdate(AssignmentSubmissionAnswerBase):
    pass

class AssignmentSubmissionAnswerInDB(AssignmentSubmissionAnswerBase):
    assignment_submission_answer_id: UUID
    assignment_submission_id: UUID
    question : AssignmentQuestionInDB
    student_id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class AssignmentSubmissionAnswer(AssignmentSubmissionAnswerInDB):
    pass
    
    
class AssignmentSubmissionInDB(AssignmentSubmissionBase):
    assignment_submission_id: UUID
    assignment_id: UUID
    student_id: UUID
    answers: List[AssignmentSubmissionAnswer]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
    
class AssignmentSubmission(AssignmentSubmissionInDB):
    pass