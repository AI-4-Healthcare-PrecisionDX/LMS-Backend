from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class DiscussionMessageBase(BaseModel):
    discussion_text: str

class DiscussionMessageCreate(DiscussionMessageBase):
    discussion_id: UUID
    user_id: UUID

class DiscussionMessage(DiscussionMessageBase):
    discussion_message_id: UUID
    created_at: datetime
    updated_at: datetime


