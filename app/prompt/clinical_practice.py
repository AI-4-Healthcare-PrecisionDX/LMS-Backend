from langfuse import Langfuse
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from app.core.config import settings


class ClinicalPracticePrompt:
    def __init__(self):
        self.langfuse = Langfuse(
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key=settings.LANGFUSE_SECRET_KEY,
            host=settings.LANGFUSE_HOST,
        )
        self.prompt = self.langfuse.get_prompt("clinical_practice")

    def get_prompt(self, scenario, scenario_examination_findings):
        clinical_practice_prompt = self.prompt.compile(
            patient_name=scenario.patient_name,
            patient_age=scenario.patient_age,
            patient_gender=scenario.patient_gender,
            patient_chief_complaint=scenario.patient_chief_complaint,
            detailed_description=scenario.detailed_description,
            vital_signs=scenario_examination_findings.vital_signs,
            general_appearance=scenario_examination_findings.general_appearance,
            cardiovascular_findings=scenario_examination_findings.cardiovascular_findings,
            lungs_findings=scenario_examination_findings.lungs_findings,
            additional_findings=scenario_examination_findings.additional_findings,
        )

        return clinical_practice_prompt[0]["content"]

    def create_prompt(
        self, scenario, scenario_examination_findings
    ) -> ChatPromptTemplate:
        system_template = self.get_prompt(scenario, scenario_examination_findings)
        # Define the variables explicitly
        prompt_messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            MessagesPlaceholder(variable_name="history"),
            MessagesPlaceholder(variable_name="messages"),
        ]
        return ChatPromptTemplate.from_messages(prompt_messages)
