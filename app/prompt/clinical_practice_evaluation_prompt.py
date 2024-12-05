# from langfuse import Langfuse
# from langchain_core.prompts import (
#     ChatPromptTemplate,
#     SystemMessagePromptTemplate,
#     HumanMessagePromptTemplate,
#     MessagesPlaceholder,
# )
# from langchain_core.messages import HumanMessage

# from app.core.config import settings


# class ClinicalPracticeEvaluationPrompt:
#     def __init__(self):
#         self.langfuse = Langfuse(
#             public_key=settings.LANGFUSE_PUBLIC_KEY,
#             secret_key=settings.LANGFUSE_SECRET_KEY,
#             host=settings.LANGFUSE_HOST,
#         )
#         self.prompt = self.langfuse.get_prompt("clinical-practice-evaluation")
        
#     def get_prompt(self, evaluation_data):
#         # (scenario_title, patient_age, patient_gender, patient_chief_complaint, detailed_description, conversation_example)= scenario
#         # (vital_signs, general_appearance,cardiovascular_findings,lungs_findings,additional_findings)= scenario_examination_findings
#         # (role, content)= thread_messages
#         # diagnosis = diagnosis
#         # treatment = treatment
#         # doctor_notes = doctor_notes
        
#         scenario_title = evaluation_data.scenario.scenario_title
#         patient_age = evaluation_data.scenario.patient_age
#         patient_gender = evaluation_data.scenario.patient_gender
#         patient_chief_complaint = evaluation_data.scenario.patient_chief_complaint
#         detailed_description = evaluation_data.scenario.detailed_description
#         # conversation_example = evaluation_data.scenario.conversation_example
        
#         vital_signs = evaluation_data.scenario_examination_findings.vital_signs
#         general_appearance = evaluation_data.scenario_examination_findings.general_appearance
#         cardiovascular_findings = evaluation_data.scenario_examination_findings.cardiovascular_findings
#         lungs_findings = evaluation_data.scenario_examination_findings.lungs_findings
#         additional_findings = evaluation_data.scenario_examination_findings.additional_findings
        
#         thread_messages = evaluation_data.thread_messages
        
#         diagnosis = evaluation_data.diagnosis
#         treatment = evaluation_data.treatment
#         doctor_notes = evaluation_data.doctor_notes
        
#         evaluation_prompt = self.prompt.compile(
#             scenario_title=scenario_title,
#             patient_age=patient_age,
#             patient_gender= patient_gender,
#             patient_chief_complaint= patient_chief_complaint,
#             detailed_description= detailed_description,
#             # conversation_example= conversation_example,
#             vital_signs= vital_signs,
#             general_appearance= general_appearance,
#             cardiovascular_findings= cardiovascular_findings,
#             lungs_findings= lungs_findings,
#             additional_findings= additional_findings,
#             thread_messages= thread_messages,
#             diagnosis= diagnosis,
#             treatment= treatment,
#             doctor_notes= doctor_notes
#         )
        
#         print("Compiled prompt 1:", evaluation_prompt[0]["content"])
#         print("Compiled prompt 2:", evaluation_prompt[1]["content"])
        
#         return (evaluation_prompt[0]["content"], evaluation_prompt[1]["content"])
    
    
#     def create_prompt(self, evaluation_data):
#         system_template, human_template = self.get_prompt(evaluation_data)
#         # Define the variables explicitly
        
#         prompt_messages = [
#             SystemMessagePromptTemplate.from_template(system_template),
#             # HumanMessagePromptTemplate.from_template(human_template),
#             MessagesPlaceholder("input"),
#         ]
#         return (ChatPromptTemplate.from_messages(prompt_messages), human_template)





from langfuse import Langfuse
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import HumanMessage

from app.core.config import settings


class ClinicalPracticeEvaluationPrompt:
    def __init__(self):
        self.langfuse = Langfuse(
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key=settings.LANGFUSE_SECRET_KEY,
            host=settings.LANGFUSE_HOST,
        )
        self.prompt = self.langfuse.get_prompt("clinical-practice-evaluation")
        
    def get_prompt(self, evaluation_data):
        
        
        evaluation_prompt = self.prompt.compile(
            scenario_title=evaluation_data["scenario_title"],
            patient_age=evaluation_data["patient_age"],
            patient_gender=evaluation_data["patient_gender"],
            patient_chief_complaint=evaluation_data["patient_chief_complaint"],
            detailed_description=evaluation_data["detailed_description"],
            vital_signs=evaluation_data["vital_signs"],
            general_appearance=evaluation_data["general_appearance"],
            cardiovascular_findings=evaluation_data["cardiovascular_findings"],
            lungs_findings=evaluation_data["lungs_findings"],
            additional_findings=evaluation_data["additional_findings"],
            thread_messages=evaluation_data["thread_messages"],
            diagnosis=evaluation_data["diagnosis"],
            treatment=evaluation_data["treatment"],
            doctor_notes=evaluation_data["doctor_notes"],
        )
        
        print("Compiled prompt 1:", evaluation_prompt[0]["content"])
        print("Compiled prompt 2:", evaluation_prompt[1]["content"])
        
        return (evaluation_prompt[0]["content"], evaluation_prompt[1]["content"])
    
    
    def create_prompt(self, evaluation_data):
        system_template, human_template = self.get_prompt(evaluation_data)
        # Define the variables explicitly
        
        prompt_messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            # HumanMessagePromptTemplate.from_template(human_template),
            MessagesPlaceholder("input"),
        ]
        return (ChatPromptTemplate.from_messages(prompt_messages), human_template)



