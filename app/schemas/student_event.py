# app/schemas/student_event.py

from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class StudentEventBase(BaseModel):
    event_title: Optional[str] = None
    event_description: Optional[str] = None
    event_topics: Optional[List[str]] = None
    event_date: Optional[datetime] = None
    event_link: Optional[str] = None

    

class StudentEventCreate(StudentEventBase):
    event_title: str
    event_date: datetime



class StudentEventUpdate(StudentEventBase):
    pass



class StudentEventInDBBase(StudentEventBase):
    event_id: Optional[UUID] = UUID  
    student_id: Optional[UUID] = UUID  
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class StudentEvent(StudentEventInDBBase):
    pass
