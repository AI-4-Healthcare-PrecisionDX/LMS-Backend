from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import uuid


class ScenarioBase(BaseModel):
    scenario_title: Optional[str] = None
    patient_name: Optional[str] = None
    patient_age: Optional[str] = None
    patient_gender: Optional[str] = None
    patient_chief_complaint: Optional[str] = None
    detailed_description: Optional[str] = None
    conversation_example: Optional[list[Dict]] = None


class ScenarioCreate(ScenarioBase):
    scenario_title: str
    patient_name: str
    patient_age: str
    patient_chief_complaint: str


class ScenarioUpdate(ScenarioBase):
    pass


class ScenarioInDBBase(ScenarioBase):
    scenario_id: uuid.UUID

    class Config:
        orm_mode = True


class Scenario(ScenarioInDBBase):
    pass


class ScenarioForStudent(BaseModel):
    scenario_id: Optional[uuid.UUID]
    scenario_title: Optional[str]
    patient_name: Optional[str]
    patient_age: Optional[str]
    patient_gender: Optional[str]
    patient_chief_complaint: Optional[str]


class ScenarioExaminationFindingBase(BaseModel):
    vital_signs: Optional[str] = None
    general_appearance: Optional[str] = None
    cardiovascular_findings: Optional[str] = None
    lungs_findings: Optional[str] = None
    additional_findings: Optional[str] = None


class ScenarioExaminationFindingCreate(ScenarioExaminationFindingBase):
    pass


class ScenarioExaminationFindingUpdate(ScenarioExaminationFindingBase):
    pass


class ScenarioExaminationFindingInDBBase(ScenarioExaminationFindingBase):
    scenario_examination_finding_id: uuid.UUID

    class Config:
        orm_mode = True


class ScenarioExaminationFinding(ScenarioExaminationFindingInDBBase):
    pass


class ScenarioWithExaminationFinding(BaseModel):
    scenario: Scenario
    scenario_examination_findings: ScenarioExaminationFinding
    # department_id: uuid.UUID
    # branch_id: uuid.UUID


class ScenarioData(BaseModel):
    scenario: ScenarioCreate
    scenario_examination_findings: ScenarioExaminationFindingCreate
    department_id: uuid.UUID


class ScenarioThreadBase(BaseModel):
    pass


class ScenarioThreadCreate(ScenarioThreadBase):
    pass


class ScenarioThreadUpdate(ScenarioThreadBase):
    pass


class ScenarioThreadInDBBase(ScenarioThreadBase):
    scenario_thread_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True


class ScenarioThread(ScenarioThreadInDBBase):
    pass


class ScenarioThreadMessageBase(BaseModel):
    content: Optional[str]


class ScenarioThreadMessageCreate(ScenarioThreadMessageBase):
    content: str = Field(..., max_length=4032)


class ScenarioThreadMessageUpdate(ScenarioThreadMessageBase):
    pass


class ScenarioThreadMessageInDBBase(ScenarioThreadMessageBase):
    scenario_thread_message_id: uuid.UUID
    role: Optional[str]

    class Config:
        orm_mode = True


class ScenarioThreadMessage(ScenarioThreadMessageInDBBase):
    pass
