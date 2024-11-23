# app/schemas/events.py

from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class EventBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    topics: Optional[List[str]] = None
    date: Optional[datetime] = None
    link: Optional[str] = None
    is_completed: Optional[bool] = False
    

class EventCreate(EventBase):
    title: str
    description: str
    date: datetime



class EventUpdate(EventBase):
    pass



class EventInDBBase(EventBase):
    event_id: Optional[UUID] = UUID  
    student_id: Optional[UUID] = UUID  
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Event(EventInDBBase):
    pass
