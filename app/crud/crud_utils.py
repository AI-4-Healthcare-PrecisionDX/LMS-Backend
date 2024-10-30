#app/crud/crud_utils.py

from typing import Any, Dict, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.global_library import GlobalLibrary
from app.schemas.library import LibraryCreate, LibraryUpdate
import uuid


class CRUDLibrary(CRUDBase[GlobalLibrary, LibraryCreate, LibraryUpdate]):
    def get_by_uuid(
        self, db: Session, *, library_id: uuid.UUID
    ) -> Optional[GlobalLibrary]:
        return (
            db.query(GlobalLibrary)
            .filter(GlobalLibrary.library_id == library_id)
            .first()
        )

    def get_by_user(
        self, db: Session, *, user_id: uuid.UUID
    ) -> Optional[GlobalLibrary]:
        return db.query(GlobalLibrary).filter(GlobalLibrary.user_id == user_id).all()

    def create_by_user(
        self,
        db: Session,
        *,
        obj_in: LibraryCreate,
        user_id: uuid.UUID,
        material_file: str
    ) -> GlobalLibrary:
        db_obj = GlobalLibrary(
            **obj_in.dict(), user_id=user_id, material_file=material_file
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all_public(self, db: Session) -> Optional[GlobalLibrary]:
        return db.query(GlobalLibrary).filter(GlobalLibrary.visibility == True).all()

    def get_all_user_created(
        self, db: Session, *, user_id: uuid.UUID
    ) -> Optional[GlobalLibrary]:
        return db.query(GlobalLibrary).filter(GlobalLibrary.user_id == user_id).all()

    def get_all_public_and_user_created(
        self, db: Session, *, user_id: uuid.UUID
    ) -> Optional[GlobalLibrary]:
        return (
            db.query(GlobalLibrary)
            .filter(
                or_(
                    GlobalLibrary.visibility == True,
                    GlobalLibrary.user_id == user_id,
                )
            )
            .all()
        )


library = CRUDLibrary(GlobalLibrary)
