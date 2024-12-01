from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import uuid


class ScenarioBase(BaseModel):
    scenario_title: Optional[str]
    patient_name: Optional[str]
    patient_age: Optional[str]
    patient_gender: Optional[str]
    patient_chief_complaint: Optional[str]
    detailed_description: Optional[str]
    conversation_example: Optional[list[Dict]]


class ScenarioCreate(ScenarioBase):
    scenario_title: str
    patient_name: str
    patient_age: str
    patient_chief_complaint: str


class ScenarioUpdate(ScenarioBase):
    pass


class ScenarioInDBBase(ScenarioBase):
    scenario_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True


class Scenario(ScenarioInDBBase):
    pass


class ScenarioExaminationFindingBase(BaseModel):
    vital_signs: Optional[str]
    general_appearance: Optional[str]
    cardiovascular_findings: Optional[str]
    lungs_findings: Optional[str]
    additional_findings: Optional[str]


class ScenarioExaminationFindingCreate(ScenarioExaminationFindingBase):
    pass


class ScenarioExaminationFindingUpdate(ScenarioExaminationFindingBase):
    pass


class ScenarioExaminationFindingInDBBase(ScenarioExaminationFindingBase):
    scenario_examination_finding_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True


class ScenarioExaminationFinding(ScenarioExaminationFindingInDBBase):
    pass


class ScenarioData(BaseModel):
    scenario: ScenarioCreate
    scenario_examination_findings: ScenarioExaminationFindingCreate


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
