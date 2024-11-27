from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models
from app.api import deps
from app.schemas.notes import Notes, NotesCreate, NotesUpdate

router = APIRouter()



@router.get("/", response_model=List[Notes])
def get_notes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_student: models.User = Depends(deps.get_current_active_student_user),
) -> Any:
    """
    Retrieve all notes.
    """
    notes = crud.notes.get_notes(db, skip=skip, limit=limit, student_id=current_student.student_id)
    return notes



@router.post("/", response_model=Notes)
def create_note(
    *,
    db: Session = Depends(deps.get_db),
    note_in: NotesCreate,
    current_student: models.User = Depends(deps.get_current_active_student_user),
) -> Any:
    """
    Create a new note.
    """
    note = crud.notes.create_note(db, obj_in=note_in, student_id=current_student.student_id)
    return note



@router.get("/{note_id}", response_model=Notes)
def read_note(
    note_id: UUID,
    db: Session = Depends(deps.get_db),
    current_student: models.User = Depends(deps.get_current_active_student_user),
) -> Any:
    """
    Get a specific note by ID.
    """
    note = crud.notes.get_note_by_id(db=db, note_id=note_id, student_id=current_student.student_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note



@router.put("/{note_id}", response_model=Notes)
def update_note(
    *,
    note_id: UUID,
    note_in: NotesUpdate,
    db: Session = Depends(deps.get_db),
    current_student: models.User = Depends(deps.get_current_active_student_user),
) -> Any:
    """
    Update a note.
    """
    # Verify the note exists and is owned by the current student
    note = crud.notes.get_note_by_id(db=db, note_id=note_id, student_id=current_student.student_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Perform the update
    updated_note = crud.notes.update_note(db=db, db_obj=note, obj_in=note_in)
    return updated_note



@router.delete("/{note_id}", response_model=dict)
def delete_note(
    note_id: UUID,
    db: Session = Depends(deps.get_db),
    current_student: models.User = Depends(deps.get_current_active_student_user),
) -> Any:
    """
    Delete a note if it belongs to the current student.
    """
    try:
        # Call the delete_note CRUD method with the ownership check
        result = crud.notes.delete_note(db=db, note_id=note_id, student_id=current_student.student_id)
        return result
    except ValueError as e:
        # If the note doesn't exist or is not owned by the student, return a 404 error
        raise HTTPException(status_code=404, detail=str(e))
