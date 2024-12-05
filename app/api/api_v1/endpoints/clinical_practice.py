from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator, List, Any
from sqlalchemy.orm import Session
import uuid

from app.api import deps
from app.crud import crud_scenario, department
from app.schemas import scenario, Department
from app.models import Student
from uuid import UUID
from app.llm import ClinicalPracticeEvaluationLLM, ClinicalPracticeLLM
from app.schemas.scenario import ScenarioEvaluationCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.crud import crud_scenario
from app.schemas import scenario
from app.models.scenario_evaluation import ScenarioEvaluation  # Import SQLAlchemy model
router = APIRouter()


# Create a thread for a scenario
@router.post("/{scenario_id}", response_model=scenario.ScenarioThread)
def create_scenario_thread(
    scenario_id: UUID,
    db: Session = Depends(deps.get_db),
    current_student=Depends(deps.get_current_active_student_user),
):
    # Check if the scenario exists
    scenario = crud_scenario.scenario.get_by_id(db=db, scenario_id=scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found"
        )

    # Create the thread
    scenario_thread = crud_scenario.scenario_thread.create_by_scenario_id(
        db=db, scenario_id=scenario_id, student_id=current_student.student_id
    )

    return scenario_thread


# Get thread messages by thread id
@router.get(
    "/thread/{thread_id}/messages", response_model=list[scenario.ScenarioThreadMessage]
)
def get_thread_by_id(
    thread_id: UUID,
    db: Session = Depends(deps.get_db),
    current_student=Depends(deps.get_current_active_student_user),
):
    thread = crud_scenario.scenario_thread.get_by_id(
        db=db, scenario_thread_id=thread_id
    )
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found"
        )

    if thread.student_id != current_student.student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to view this thread",
        )

    thread_messages = crud_scenario.scenario_thread_message.get_multi_by_thread_id(
        db=db, scenario_thread_id=thread_id
    )
    if not thread_messages:
        return []

    return thread_messages


@router.get("/threads", response_model=List[scenario.ScenarioThread])
def get_threads(
    db: Session = Depends(deps.get_db),
    current_student=Depends(deps.get_current_active_student_user),
):
    threads = crud_scenario.scenario_thread.get_multi_by_student_id(
        db=db, student_id=current_student.student_id
    )
    if not threads:
        return []

    return threads


# Get case details
@router.get("/thread/{thread_id}", response_model=scenario.ScenarioForStudent)
def get_case_details(
    thread_id: UUID,
    db: Session = Depends(deps.get_db),
    current_student=Depends(deps.get_current_active_student_user),
):
    thread = crud_scenario.scenario_thread.get_by_id(
        db=db, scenario_thread_id=thread_id
    )
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found"
        )

    # Get the scenario using thread id
    scenario = crud_scenario.scenario.get_by_id(db=db, scenario_id=thread.scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found"
        )

    return scenario


@router.post("/thread/{thread_id}/message")
async def create_thread_message(
    thread_id: UUID,
    thread_message_in: scenario.ScenarioThreadMessageCreate,
    db: Session = Depends(deps.get_db),
    current_student=Depends(deps.get_current_active_student_user),
):
    try:
        # Check if the thread exists
        thread = crud_scenario.scenario_thread.get_by_id(
            db=db, scenario_thread_id=thread_id
        )
        if not thread:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found"
            )

        if thread.student_id != current_student.student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to view this thread",
            )

        # Get all the thread messages
        thread_messages = crud_scenario.scenario_thread_message.get_multi_by_thread_id(
            db=db, scenario_thread_id=thread_id
        )

        # Get the scenario using scenario id
        scenario_data = crud_scenario.scenario.get_by_id(
            db=db, scenario_id=thread.scenario_id
        )

        # Get the scenario examination findings using scenario id
        scenario_examination_findings_data = (
            crud_scenario.scenario_examination_finding.get_by_scenario_id(
                db=db, scenario_id=thread.scenario_id
            )
        )

        # Initialize chat
        chat = ClinicalPracticeLLM(
            session_id=str(thread_id),
            scenario=scenario_data,
            scenario_examination_findings=scenario_examination_findings_data,
        )

        async def stream_response() -> AsyncGenerator[str, None]:
            full_response = ""
            async for chunk in chat.generate_response_stream(
                question=thread_message_in.content, thread_messages=thread_messages
            ):
                full_response += chunk
                yield f"data: {chunk}\n\n"

            # Create the doctor's message
            doctor_message = crud_scenario.scenario_thread_message.create_by_thread_id(
                db=db,
                scenario_thread_id=thread_id,
                obj_in=thread_message_in,
                role="doctor",
            )
            # Create the patient's response message after receiving full response
            patient_message_in = scenario.ScenarioThreadMessageCreate(
                content=full_response
            )
            patient_message = crud_scenario.scenario_thread_message.create_by_thread_id(
                db=db,
                scenario_thread_id=thread_id,
                obj_in=patient_message_in,
                role="patient",
            )

            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_response(), media_type="text/event-stream")

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in create_thread_message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the thread message",
        )


@router.get("/departments", response_model=List[Department])
def read_departments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Student = Depends(deps.get_current_active_student_user),
) -> Any:
    """
    Retrieve departments.
    """
    try:
        departments = department.get_departments_for_student(
            db, user_id=current_user.user_id, skip=skip, limit=limit
        )
        if not departments:
            return []
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the departments",
        )
    return departments


@router.get(
    "/department/{department_id}/scenarios",
    response_model=List[scenario.ScenarioForStudent],
)
def read_department_scenarios(
    department_id: UUID,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Student = Depends(deps.get_current_active_student_user),
) -> Any:
    """
    Retrieve department scenarios.
    """
    try:
        department_data = department.get_department_for_student(
            db, user_id=current_user.user_id, department_id=department_id
        )
        if not department_data:
            raise HTTPException(status_code=404, detail="Department not found")

        scenarios = crud_scenario.scenario.get_scenario_by_department_id(
            db, department_id=department_id, skip=0, limit=100
        )
        if not scenarios:
            return []
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while retrieving the department scenarios",
        )
    return scenarios




# # create an endpoint to evaluate the clinical practice
# @router.post("/get/evaluate/")
# def evaluate_clinical_practice(
#     evaluation_data: scenario.ClinicalPracticeEvaluationCreate,
#     # db: Session = Depends(deps.get_db),
#     # current_student=Depends(deps.get_current_active_student_user),
# ):
#     # This will be replaced with a thread_id
#     session_id = uuid.uuid4()
#     llm = ClinicalPracticeEvaluationLLM(
#         evaluation_data=evaluation_data, scenario_thread_id=str(session_id)
#     )

#     evaluation = llm.evaluate_clinical_practice()

#     return evaluation


# create an endpoint to evaluate the clinical practice
# app/api/api_v1/endpoints/clinical_practice.py



@router.post("/get/evaluation", response_model=scenario.ScenarioEvaluation)
def evaluate_clinical_practice(
    evaluation_data: scenario.ClinicalPracticeEvaluationCreate,
    db: Session = Depends(deps.get_db),
):
    scenario_thread_id = evaluation_data.scenario_thread_id
    
    # Get scenario and thread data
    scenario_thread = crud_scenario.scenario_thread.get_by_id(
        db=db, 
        scenario_thread_id=scenario_thread_id
    )
    
    scenario_data = crud_scenario.scenario.get_scenario_with_findings_by_scenario_id(
        db=db, 
        scenario_id=scenario_thread.scenario_id
    )
    
    thread_data = crud_scenario.scenario_thread.get_thread_with_messages_by_scenario_id(
        db=db, 
        scenario_thread_id=scenario_thread_id
    )
    
    # Prepare evaluation data
    llm_evaluation_data = {
        "scenario_title": scenario_data.scenario_title,
        "patient_age": scenario_data.patient_age,
        "patient_gender": scenario_data.patient_gender,
        "patient_chief_complaint": scenario_data.patient_chief_complaint,
        "detailed_description": scenario_data.detailed_description,
        "vital_signs": scenario_data.scenario_examination_findings.vital_signs,
        "general_appearance": scenario_data.scenario_examination_findings.general_appearance,
        "cardiovascular_findings": scenario_data.scenario_examination_findings.cardiovascular_findings,
        "lungs_findings": scenario_data.scenario_examination_findings.lungs_findings,
        "additional_findings": scenario_data.scenario_examination_findings.additional_findings,
        "thread_messages": thread_data,
        "diagnosis": evaluation_data.diagnosis,
        "treatment": evaluation_data.treatment,
        "doctor_notes": evaluation_data.doctor_notes
    }
    
    # Get evaluation from LLM
    llm = ClinicalPracticeEvaluationLLM(
        evaluation_data=llm_evaluation_data,
        scenario_thread_id=str(scenario_thread_id)
    )

    llm_evaluation = llm.evaluate_clinical_practice()
    
    # Create evaluation data for database
    evaluation_create_data = {
        "thread_id": scenario_thread_id,
        "conversation_relevance_of_replies_score": llm_evaluation["conversation_evaluation"]["relevance_of_replies_score"],
        "conversation_medical_accuracy_of_replies_score": llm_evaluation["conversation_evaluation"]["medical_accuracy_of_replies_score"],
        "conversation_communication_clarity_score": llm_evaluation["conversation_evaluation"]["communication_clarity_score"],
        "conversation_empathy_and_professionalism_score": llm_evaluation["conversation_evaluation"]["empathy_and_professionalism_score"],
        "conversation_constructive_feedback": llm_evaluation["conversation_evaluation"]["constructive_feedback"],
        
        "diagnosis_relevance_score": llm_evaluation["diagnosis_evaluation"]["relevance_score"],
        "diagnosis_accuracy_score": llm_evaluation["diagnosis_evaluation"]["accuracy_score"],
        "diagnosis_constructive_feedback": llm_evaluation["diagnosis_evaluation"]["constructive_feedback"],
        
        "treatment_relevance_score": llm_evaluation["treatment_evaluation"]["relevance_score"],
        "treatment_effectiveness_score": llm_evaluation["treatment_evaluation"]["effectiveness_score"],
        "treatment_constructive_feedback": llm_evaluation["treatment_evaluation"]["constructive_feedback"],
        
        "notes_clarity_score": llm_evaluation["notes_evaluation"]["clarity_score"],
        "notes_completeness_score": llm_evaluation["notes_evaluation"]["completeness_score"],
        "notes_constructive_feedback": llm_evaluation["notes_evaluation"]["constructive_feedback"],
        
        "overall_score": llm_evaluation["overall_performance"]["overall_score"],
        "overall_constructive_feedback": llm_evaluation["overall_performance"]["constructive_feedback"],
        "time_management": llm_evaluation["overall_performance"]["additional_notes"]["time_management"],
        "other_observations": llm_evaluation["overall_performance"]["additional_notes"]["other_observations"]
    }
    
    # Save evaluation to database
    evaluation = crud_scenario.scenario_evaluation.create_evaluation(
        db=db,
        obj_in=evaluation_create_data
    )

    return evaluation

@router.get("/ongoing-evaluation/{thread_id}")
def ongoing_evaluation(
    thread_id: UUID,
    db: Session = Depends(deps.get_db),
    current_student=Depends(deps.get_current_active_student_user),
):
    
    # Check if the thread exists in the evaluation table
    evaluation = crud_scenario.scenario_evaluation.get_by_thread_id(
        db=db, scenario_thread_id=thread_id
    )
        