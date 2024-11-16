from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class AssignmentQuestionGeneration(BaseModel):
    """
    Pydantic model for representing a generated question
    """

    type: str = Field(
        ...,
        description="Type of question (question_bank, adaptive_learning, application_based, writing_assignment, scenario_based)",
    )
    mcq: bool = Field(..., description="Whether the question is multiple choice")
    difficulty: str = Field(
        ..., description="Difficulty level of the question (easy, medium, hard)"
    )
    question: str = Field(
        ...,
        description="The actual question text",
    )
    options: List[str] = Field(
        ...,
        description="List of possible answer options or empty list if not multiple choice",
    )
    correct_answers: List[str] = Field(
        ...,
        description="List of correct answers",
    )
    explanation: Optional[str] = Field(
        None, description="Explanation of the correct answer"
    )


class AssignmentQuestionSet(BaseModel):
    questions: List[AssignmentQuestionGeneration] = Field(
        ..., description="List of generated questions"
    )
