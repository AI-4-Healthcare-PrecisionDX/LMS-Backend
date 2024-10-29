from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app import crud, models
from app.api import deps
from app.schemas.discussion_message import DiscussionMessage, DiscussionMessageCreate
from app.schemas.discussion_reply_message import DiscussionReplyMessage, DiscussionReplyMessageCreate

router = APIRouter()

@router.get("/messages/", response_model=List[DiscussionMessage])
def get_discussion_messages(
    discussion_id: UUID,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all messages for a specific discussion.
    """
    messages = crud.discussion_message.get_messages_by_discussion(db, discussion_id=discussion_id, skip=skip, limit=limit)
    return messages

@router.post("/messages/", response_model=DiscussionMessage)
def create_discussion_message(
    *,
    db: Session = Depends(deps.get_db),
    message_in: DiscussionMessageCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new message in a discussion.
    """
    message = crud.discussion_message.create_message(db, obj_in=message_in, user_id=current_user.user_id)
    return message

@router.get("/messages/{message_id}", response_model=DiscussionMessage)
def read_discussion_message(
    message_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific message by ID.
    """
    message = crud.discussion_message.get_message_by_id(db=db, id=message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.delete("/messages/{message_id}", response_model=dict)
def delete_discussion_message(
    message_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a message (Only for the message creator).
    """
    message = crud.discussion_message.get_message_by_id(db=db, id=message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    if current_user.user_id != message.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this message")

    crud.discussion_message.delete_message(db, id=message_id, user_id=current_user.user_id)
    return {"message": "Message deleted successfully"}


@router.get("/replies/", response_model=List[DiscussionReplyMessage])
def get_message_replies(
    discussion_message_id: UUID,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all replies for a specific message.
    """
    replies = crud.discussion_reply_message.get_replies_by_message(db, discussion_message_id=discussion_message_id, skip=skip, limit=limit)
    return replies

@router.post("/replies/", response_model=DiscussionReplyMessage)
def create_message_reply(
    *,
    db: Session = Depends(deps.get_db),
    reply_in: DiscussionReplyMessageCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a reply to a message.
    """
    reply = crud.discussion_reply_message.create_reply(db, obj_in=reply_in, user_id=current_user.user_id)
    return reply

@router.get("/replies/{reply_id}", response_model=DiscussionReplyMessage)
def read_message_reply(
    reply_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific reply by ID.
    """
    reply = crud.discussion_reply_message.get_reply_by_id(db=db, id=reply_id)
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found")
    return reply

@router.delete("/replies/{reply_id}", response_model=dict)
def delete_message_reply(
    reply_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a reply (Only for the reply creator).
    """
    reply = crud.discussion_reply_message.get_reply_by_id(db=db, id=reply_id)
    if not reply:
        raise HTTPException(status_code=404, detail="Reply not found")

    if current_user.user_id != reply.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this reply")

    crud.discussion_reply_message.delete_reply(db, id=reply_id, user_id=current_user.user_id)
    return {"message": "Reply deleted successfully"}
