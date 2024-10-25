from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class DiscussionReplyMessageBase(BaseModel):
    discussion_reply_text: str

class DiscussionReplyMessageCreate(DiscussionReplyMessageBase):
    discussion_message_id: UUID
    user_id: UUID

class DiscussionReplyMessage(DiscussionReplyMessageBase):
    discussion_reply_message_id: UUID
    created_at: datetime
    updated_at: datetime


