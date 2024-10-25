from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class DiscussionCreate(BaseModel):
    section_id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None



class DiscussionUpdate(BaseModel):
    section_id: Optional[UUID] = None



class Discussion(BaseModel):
    discussion_id: UUID
    section_id: UUID
    created_at: datetime
    updated_at: datetime


