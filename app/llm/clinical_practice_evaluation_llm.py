from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import PydanticOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import pypdf
import json
from langfuse.callback import CallbackHandler
from langchain_core.runnables import RunnablePassthrough
import random
import time
from langchain_core.messages import HumanMessage, SystemMessage

from app.core.config import settings
from app.prompt import ClinicalPracticeEvaluationPrompt
from app.schemas.llm import EvaluationOutput
from app.data import assignment_question_generate as assignment
import logging
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from app.llm.prompts.load_prompt import load_yaml_prompt

logging.basicConfig(level=logging.INFO)


class ClinicalPracticeEvaluationLLM:
    def __init__(self, evaluation_data, scenario_thread_id, scenario_title):
        self.llm = ChatOpenAI(
            model="gpt-4.1",
            temperature=0,
        )
        self.scenario_thread_id = scenario_thread_id

        self.evaluation_system_prompt = load_yaml_prompt("clinical_practice_evaluation", "SYSTEM_PROMPT")
        self.evaluation_human_prompt = load_yaml_prompt("clinical_practice_evaluation", "USER_PROMPT")

        self.output_parser = PydanticOutputParser(pydantic_object=EvaluationOutput)
        # self.embeddings = OpenAIEmbeddings()
        self.evaluation_data = evaluation_data
        self.scenario_title = scenario_title

    def evaluate_clinical_practice(self):
        prompt = [
            SystemMessage(content=self.evaluation_system_prompt.format(scenario_title=self.scenario_title)),
            HumanMessage(content=self.evaluation_human_prompt.format(**self.evaluation_data)),
        ]
        response = self.llm.with_structured_output(EvaluationOutput).invoke(prompt)
        return response.evaluation_result
