from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.notes import Notes
from app.schemas.notes import NotesCreate, NotesUpdate
import uuid


class CRUDNotes(CRUDBase[Notes, NotesCreate, NotesUpdate]):
    def get_note_by_id(self, db: Session, *, note_id: uuid.UUID, student_id: uuid.UUID) -> Optional[Notes]:
        return db.query(Notes).filter(Notes.note_id == note_id, Notes.student_id == student_id).first()

    def create_note(self, db: Session, *, obj_in: NotesCreate, student_id:uuid.UUID) -> Notes:
        db_obj = Notes(
            note_title=obj_in.note_title,
            note_teacher=obj_in.note_teacher,
            note_content=obj_in.note_content,
            note_markdown_content=obj_in.note_markdown_content,
            student_id = student_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    
    def get_notes(self, db: Session, *, student_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[Notes]:
        """
        Retrieve all notes for a specific student.
        """
        return (
            db.query(Notes)
            .filter(Notes.student_id == student_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
    def update_note(self, db: Session, *, db_obj: Notes, obj_in: NotesUpdate) -> Notes:
        """
        Update an existing note.
        """
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    
    def delete_note(self, db: Session, *, note_id: uuid.UUID, student_id: uuid.UUID) -> Dict[str, Any]:
        """
        Delete a note only if it belongs to the current student.
        """
        note = db.query(Notes).filter(Notes.note_id == note_id, Notes.student_id == student_id).first()
        if not note:
            raise ValueError("Note not found or not owned by the student")

        db.delete(note)
        db.commit()
        return {"message": "Note deleted successfully"}


notes = CRUDNotes(Notes)
