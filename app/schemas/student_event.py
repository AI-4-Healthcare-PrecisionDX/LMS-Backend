# app/schemas/student_event.py

from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class StudentEventBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    topics: Optional[List[str]] = None
    date: Optional[datetime] = None
    link: Optional[str] = None
    is_completed: Optional[bool] = False
    

class StudentEventCreate(StudentEventBase):
    title: str
    description: str
    date: datetime



class StudentEventUpdate(StudentEventBase):
    pass



class StudentEventInDBBase(StudentEventBase):
    event_id: Optional[UUID] = UUID  
    student_id: Optional[UUID] = UUID  
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StudentEvent(StudentEventInDBBase):
    pass
