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
from langchain_core.messages import HumanMessage

from app.core.config import settings
from app.prompt import ClinicalPracticeEvaluationPrompt
from app.schemas.llm import EvaluationOutput
from app.data import assignment_question_generate as assignment
import logging

logging.basicConfig(level=logging.INFO)


class ClinicalPracticeEvaluationLLM:
    def __init__(self, evaluation_data, thread_id):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=0,
        )
        self.thread_id = thread_id

        self.evaluation_prompt = ClinicalPracticeEvaluationPrompt()

        self.output_parser = PydanticOutputParser(pydantic_object=EvaluationOutput)
        self.embeddings = OpenAIEmbeddings()
        self.evaluation_data = evaluation_data

    def evaluate_clinical_practice(self):
        start = time.time()

        evaluation_data = self.evaluation_data

        prompt, human_msg = self.evaluation_prompt.create_prompt(evaluation_data)

        chain = prompt | self.llm | self.output_parser

        langfuse_handler = CallbackHandler()
        # Only pass the input variable as that's all that's needed
        evaluation = chain.invoke(
            {"input": [HumanMessage(content=human_msg)]},
            config={
                "configurable": {"session_id": self.thread_id},
                "callbacks": [langfuse_handler],
                "run_name": "chat_evaluation",
                "tags": [
                    "chat_evaluation",
                    settings.OPENAI_MODEL,
                ],
                "metadata": {
                    "langfuse_session_id": str(self.thread_id),
                },
            },
        )

        return evaluation.evaluation_result
