from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.discussion import Discussion
from app.schemas.discussion import DiscussionCreate, DiscussionUpdate
from app.models.user import User
import uuid


class CRUDDiscussion(CRUDBase[Discussion, DiscussionCreate, DiscussionUpdate]):

    def get_discussion_by_id(self, db: Session, *, id: str) -> Optional[Discussion]:
        return db.query(Discussion).filter(Discussion.discussion_id == id).first()

    def get_multi(self, db: Session, *, skip=0, limit=100):
        return super().get_multi(db, skip=skip, limit=limit)

    def create_discussion(self, db: Session, *, obj_in: DiscussionCreate, user_id: uuid.UUID) -> Discussion:
        # Retrieve the user and check their role for authorization
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user or user.role not in ["admin", "teacher"]:
            raise ValueError("User is not authorized to create discussions")

        # Create the discussion
        db_obj = Discussion(
            section_id=obj_in.section_id,
            created_at=obj_in.created_at,
            updated_at=obj_in.updated_at
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj



    def delete_discussion(self, db: Session, *, id: str, user_id: uuid.UUID) -> Dict[str, Any]:

        discussion = db.query(Discussion).filter(Discussion.discussion_id == id).first()
        if not discussion:
            raise ValueError("Discussion not found")

        user = db.query(User).filter(User.user_id == user_id).first()


        # Delete the discussion
        db.delete(discussion)
        db.commit()
        return {"message": "Discussion deleted successfully"}


# Instantiate CRUDDiscussion for use in API calls
discussion = CRUDDiscussion(Discussion)
