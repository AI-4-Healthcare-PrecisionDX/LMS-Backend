from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator


from app.api import deps
from app.crud import crud_scenario
from app.schemas import scenario
from uuid import UUID
from app.llm import ClinicalPracticeLLM


router = APIRouter()


@router.post("/create_scenario")
def create_scenario(
    scenario_in: scenario.ScenarioData,
    db=Depends(deps.get_db),
    # current_teacher=Depends(deps.get_current_active_teacher_user),
):
    # Get the scenario from scene_in
    scenario = scenario_in.scenario
    # Get the scenario_examination_findings from scene_in
    scenario_examination_findings = scenario_in.scenario_examination_findings

    # Create the scenario
    scenario = crud_scenario.scenario.create(db=db, obj_in=scenario)
    # Create the scenario_examination_findings
    scenario_examination_findings = crud_scenario.scenario_examination_finding.create(
        db=db, obj_in=scenario_examination_findings
    )

    return {"detail": "Scenario created successfully"}


# Get all scenarios
@router.get("/scenarios")
def get_all_scenarios(
    db=Depends(deps.get_db),
    # current_teacher=Depends(deps.get_current_active_teacher_user),
):
    scenarios = crud_scenario.scenario.get_multi(db=db)
    scenario_examination_findings = (
        crud_scenario.scenario_examination_finding.get_multi(db=db)
    )
    return {
        "scenarios": scenarios,
        "scenario_examination_findings": scenario_examination_findings,
    }


# Create a thread for a scenario
@router.post("/{scenario_id}", response_model=scenario.ScenarioThread)
def create_scenario_thread(
    scenario_id: UUID,
    db=Depends(deps.get_db),
    # current_student=Depends(deps.get_current_active_student_user),
):
    # Check if the scenario exists
    scenario = crud_scenario.scenario.get_by_id(db=db, scenario_id=scenario_id)
    if not scenario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found"
        )

    # Create the thread
    scenario_thread = crud_scenario.scenario_thread.create_by_scenario_id(
        db=db, scenario_id=scenario_id
    )

    return scenario_thread


# Get thread messages by thread id
@router.get("/thread/{thread_id}", response_model=list[scenario.ScenarioThreadMessage])
def get_thread_by_id(
    thread_id: UUID,
    db=Depends(deps.get_db),
    # current_student=Depends(deps.get_current_active_student_user),
):
    thread = crud_scenario.scenario_thread.get_by_id(
        db=db, scenario_thread_id=thread_id
    )
    if not thread:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found"
        )

    thread_messages = crud_scenario.scenario_thread_message.get_multi_by_thread_id(
        db=db, scenario_thread_id=thread_id
    )

    return thread_messages


@router.post("/thread/{thread_id}")
async def create_thread_message(
    thread_id: UUID,
    thread_message_in: scenario.ScenarioThreadMessageCreate,
    db=Depends(deps.get_db),
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
