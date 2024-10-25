from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models
from app.api import deps
from app.schemas.discussion import Discussion, DiscussionCreate , DiscussionUpdate 

router = APIRouter()

@router.get("/", response_model=List[Discussion])
def get_discussions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all discussions.
    """
    discussions = crud.discussion.get_multi(db, skip=skip, limit=limit)
    return discussions

@router.post("/", response_model=Discussion) 
def create_discussion(
    *,
    db: Session = Depends(deps.get_db),
    discussion_in: DiscussionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new discussion (Only for admins and teachers).
    """
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=403,
            detail="Only admins and teachers can create discussions",
        )

    discussion = crud.discussion.create_discussion(db, obj_in=discussion_in, user_id=current_user.user_id)
    return discussion


@router.get("/{discussion_id}", response_model=Discussion)
def read_discussion(
    discussion_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific discussion by ID.
    """
    discussion = crud.discussion.get_discussion_by_id(db=db, id=discussion_id)
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")
    return discussion

@router.delete("/{discussion_id}", response_model=dict)
def delete_discussion(
    discussion_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a discussion (Only for admins or the creator).
    """
    discussion = crud.discussion.get_discussion_by_id(db=db, id=discussion_id)
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")
    
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to delete this discussion",
        )

    crud.discussion.delete_discussion(db, id=discussion_id, user_id=current_user.user_id)
    return {"message": "Discussion deleted successfully"}

