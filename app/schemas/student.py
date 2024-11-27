# app/schemas/student.py

from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime



class StudentBase(BaseModel):
    enrollment_year: Optional[int] = None
    metric_id: Optional[str] = None



class StudentCreate(StudentBase):
    enrollment_year: int
    metric_id: str



class StudentUpdate(StudentBase):
    pass



class StudentInDBBase(StudentBase):
    student_id: Optional[UUID] = UUID  
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Student(StudentInDBBase):
    pass
