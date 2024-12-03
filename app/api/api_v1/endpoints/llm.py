from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session


from app.api import deps
from app.llm import QuestionLLM, ClinicalPracticeLLM
from app import models

import uuid

router = APIRouter()


@router.post("/assignment_questions")
def create_questions(
    pdf_file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    # current_user: models.User = Depends(deps.get_current_active_user),
    question_bank_mcq: int = Form(...),
    question_bank_broad: int = Form(...),
    adaptive_learning_mcq: int = Form(...),
    adaptive_learning_broad: int = Form(...),
    application_based_mcq: int = Form(...),
    application_based_broad: int = Form(...),
    writing_assignment_mcq: int = Form(...),
    writing_assignment_broad: int = Form(...),
    scenario_based_mcq: int = Form(...),
    scenario_based_broad: int = Form(...),
    total_mcq_questions: int = Form(...),
    total_broad_questions: int = Form(...),
):
    if pdf_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    question_type_count = (
        question_bank_mcq,
        question_bank_broad,
        adaptive_learning_mcq,
        adaptive_learning_broad,
        application_based_mcq,
        application_based_broad,
        writing_assignment_mcq,
        writing_assignment_broad,
        scenario_based_mcq,
        scenario_based_broad,
        total_mcq_questions,
        total_broad_questions,
    )
    session_id = uuid.uuid4()
    llm = QuestionLLM(
        question_type_count=question_type_count,
        pdf_file=pdf_file,
        session_id=str(session_id),
    )

    questions, metadata = llm.generate_questions()

    # print(questions)

    return {"questions": questions, "metadata": metadata}
