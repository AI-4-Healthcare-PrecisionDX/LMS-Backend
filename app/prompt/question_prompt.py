from langfuse import Langfuse
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import HumanMessage

from app.core.config import settings


class QuestionPrompt:
    def __init__(self):
        self.langfuse = Langfuse(
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key=settings.LANGFUSE_SECRET_KEY,
            host=settings.LANGFUSE_HOST,
        )
        self.prompt = self.langfuse.get_prompt("assignment-creation")

    def get_prompt(self, question_type_count):
        (
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
        ) = question_type_count

        question_prompt = self.prompt.compile(
            question_bank_mcq=question_bank_mcq,
            question_bank_broad=question_bank_broad,
            adaptive_learning_mcq=adaptive_learning_mcq,
            adaptive_learning_broad=adaptive_learning_broad,
            application_based_mcq=application_based_mcq,
            application_based_broad=application_based_broad,
            writing_assignment_mcq=writing_assignment_mcq,
            writing_assignment_broad=writing_assignment_broad,
            scenario_based_mcq=scenario_based_mcq,
            scenario_based_broad=scenario_based_broad,
        )
        # Add debug logging
        # print("Compiled prompt:", question_prompt)

        return question_prompt[0]["content"]

    def create_prompt(self, question_type_count) -> ChatPromptTemplate:
        system_template = self.get_prompt(question_type_count)
        # Define the variables explicitly
        prompt_messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            MessagesPlaceholder("content"),
            MessagesPlaceholder("format_instructions"),
        ]
        return ChatPromptTemplate.from_messages(prompt_messages)
