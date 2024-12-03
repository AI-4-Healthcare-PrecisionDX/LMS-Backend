from typing import Optional, List, Dict
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


class Configuration(BaseModel):
    """Configuration model for question counts"""

    total_mcq_questions: int = Field(ge=0)
    total_broad_questions: int = Field(ge=0)
    question_bank_mcq: int = Field(ge=0)
    question_bank_broad: int = Field(ge=0)
    adaptive_learning_mcq: int = Field(ge=0)
    adaptive_learning_broad: int = Field(ge=0)
    application_based_mcq: int = Field(ge=0)
    application_based_broad: int = Field(ge=0)
    writing_assignment_mcq: int = Field(ge=0)
    writing_assignment_broad: int = Field(ge=0)
    scenario_based_mcq: int = Field(ge=0)
    scenario_based_broad: int = Field(ge=0)


class Metadata(BaseModel):
    """Metadata for the question set"""

    total_questions: int = Field(..., ge=1)
    configuration: Configuration


class AssignmentQuestionSet(BaseModel):
    questions: List[AssignmentQuestionGeneration] = Field(
        ..., description="List of generated questions"
    )
    metadata: Metadata = Field(..., description="Metadata about the question set")



class ConversationEvaluation(BaseModel):
    relevance_of_replies_score: float
    medical_accuracy_of_replies_score: float
    communication_clarity_score: float
    empathy_and_professionalism_score: float
    strengths: List[str]
    weaknesses: List[str]

class DiagnosisEvaluation(BaseModel):
    relevance_score: float
    accuracy_score: float
    strengths: List[str]
    weaknesses: List[str]

class TreatmentEvaluation(BaseModel):
    relevance_score: float
    effectiveness_score: float
    strengths: List[str]
    weaknesses: List[str]

class NotesEvaluation(BaseModel):
    clarity_score: float
    completeness_score: float
    strengths: List[str]
    weaknesses: List[str]

class AdditionalNotes(BaseModel):
    time_management: str
    other_observations: str

class OverallPerformance(BaseModel):
    overall_score: float
    missed_opportunities: List[str]
    overall_feedback: str
    additional_notes: AdditionalNotes

class EvaluationResult(BaseModel):
    conversation_evaluation: ConversationEvaluation
    diagnosis_evaluation: DiagnosisEvaluation
    treatment_evaluation: TreatmentEvaluation
    notes_evaluation: NotesEvaluation
    overall_performance: OverallPerformance
    
    
class EvaluationOutput(BaseModel):
    evaluation_result: EvaluationResult
    