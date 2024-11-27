from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class NotesBase(BaseModel):
    note_title: str
    note_teacher: str
    note_content: Optional[str] = None
    note_markdown_content: Optional[str] = None


class NotesCreate(NotesBase):
    pass


class NotesUpdate(BaseModel):
    note_title: Optional[str] = None
    note_teacher: Optional[str] = None
    note_content: Optional[str] = None
    note_markdown_content: Optional[str] = None


class Notes(NotesBase):
    note_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
