from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models
from app.api import deps
from app.schemas.section import (
    Section,

) 
from app.schemas.assignment_submission import (
    AssignmentSubmissionBase,
    AssignmentSubmissionCreate,
    AssignmentSubmissionUpdate,
    AssignmentSubmissionAnswerBase,
    AssignmentSubmissionAnswerCreate,
    AssignmentSubmissionAnswerUpdate,
    AssignmentSubmissionAnswerInDB,
    AssignmentSubmissionAnswer,
    AssignmentSubmissionInDB,
    AssignmentSubmission
)

router = APIRouter()


@router.post("/join-section", response_model=Section)
def join_section(
    *,
    db: Session = Depends(deps.get_db),
    section_code: str,
    current_student: models.User = Depends(deps.get_current_active_student_user),
) -> Any:
    """
    Join a section (Only for authorized users).
    """

    try:
        section = crud.section.join_section(
            db, section_code=section_code, student_id=current_student.student_id
        )
        return section
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/get-sections", response_model=List[Section])
def get_sections(
    db: Session = Depends(deps.get_db),
    current_student: models.User = Depends(deps.get_current_active_student_user),
) -> Any:
    
    
    try:
        sections = crud.section.get_sections_for_student(db, student_id=current_student.student_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return sections




# #create and endpoint for assignment submission
# @router.post("/submit-assignment")
# def submit_assignment(
#     *,
#     db: Session = Depends(deps.get_db),
#     assignment_submission_in: ,
#     current_student: models.User = Depends(deps.get_current_active_student_user),
# ) -> Any:
#     """
#     Submit an assignment.
#     """
    
#     try:
#         assignment_submission = crud.assignment_submission.create(
#             db, obj_in=assignment_submission_in, student_id=current_student.student_id
#         )
#         return assignment_submission
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
#     return assignment_submission