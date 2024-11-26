from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models
from app.api import deps
from app.schemas.student_event import (
    StudentEvent,
    StudentEventCreate,
    StudentEventUpdate,
) 

router = APIRouter()


@router.get("/", response_model=List[StudentEvent])
def get_student_events(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all student events.
    """
    events = crud.student_event.get_multi(db, skip=skip, limit=limit)
    return events


@router.post("/create-student-event", response_model=StudentEvent)
def create_student_event(
    *,
    db: Session = Depends(deps.get_db),
    event_in: StudentEventCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new student event (Only for authorized users).
    """
    try:
        event = crud.student_event.create_student_event(
            db, obj_in=event_in, student_id=current_user.user_id
        )
    except Exception as e:
        print(f"Error creating student event: {str(e)}")  # Log the specific error
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the student event: {str(e)}",
        )
    return event


@router.put("/update-student-event/{event_id}", response_model=StudentEvent)
def update_student_event(
    *,
    db: Session = Depends(deps.get_db),
    event_id: UUID,
    event_in: StudentEventUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a student event.
    """
    event = crud.student_event.get_student_event_by_id(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Student event not found")

    try:
        updated_event = crud.student_event.update_student_event(
            db, db_obj=event, obj_in=event_in
        )
    except Exception as e:
        print(f"Error updating student event: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while updating the student event: {str(e)}",
        )
    return updated_event


@router.get("/get-student-event/{event_id}", response_model=StudentEvent)
def read_student_event(
    event_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a specific student event by ID.
    """
    event = crud.student_event.get_student_event_by_id(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Student event not found")
    return event


@router.delete("/delete-student-event/{event_id}")
def delete_student_event(
    event_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a student event.
    """
    event = crud.student_event.get_student_event_by_id(db=db, id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Student event not found")

    try:
        crud.student_event.delete_student_event(db, id=event_id)
    except Exception as e:
        print(f"Error deleting student event: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the student event: {str(e)}",
        )
    return {"message": "Student event deleted successfully"}
