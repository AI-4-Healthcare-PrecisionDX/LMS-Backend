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


from app.core.config import settings
from app.prompt import QuestionPrompt
from app.schemas.llm import AssignmentQuestionSet
from app.data import assignment_question_generate as assignment
import logging

logging.basicConfig(level=logging.INFO)


class QuestionLLM:
    def __init__(self, question_type_count, pdf_file, session_id):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=0,
        )
        self.session_id = session_id

        self.question_prompt = QuestionPrompt()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=200
        )
        self.output_parser = PydanticOutputParser(pydantic_object=AssignmentQuestionSet)
        self.embeddings = OpenAIEmbeddings()
        self.pdf = pdf_file
        self.question_type_count = question_type_count

    # def preprocess_pdf(self):
    #     plain_text = ""
    #     pdf_reader = pypdf.PdfReader(self.pdf.file)
    #     for page in pdf_reader.pages:
    #         plain_text += page.extract_text()

    #     chunks = self.text_splitter.split_text(plain_text)
    #     vector_store = FAISS.from_texts(chunks, self.embeddings)
    #     retriever = vector_store.as_retriever()
    #     return retriever

    def preprocess_pdf(self):
        text = ""
        pypdf_loader = pypdf.PdfReader(self.pdf.file)
        for page in pypdf_loader.pages:
            page_text = page.extract_text()
            # remove '{' and '}' from the page_text
            page_text = page_text.replace("{", " ").replace("}", " ")
            text += page_text

        splits = self.text_splitter.split_text(text)
        # Number of question greater than N.
        selected_splits = min(6, len(splits))
        sampled_splits = random.sample(splits, selected_splits)
        return sampled_splits

    def format_docs(self, splits):
        return "\n\n".join([split for split in splits])

    def generate_questions(self):
        start = time.time()
        splits = self.preprocess_pdf()

        logging.info(f"Preprocessing time: {time.time() - start}")

        start = time.time()
        content = self.format_docs(splits)
        logging.info(f"Formatting time: {time.time() - start}")
        # format_instructions = self.output_parser.get_format_instructions()

        prompt = self.question_prompt.create_prompt(content, self.question_type_count)

        logging.info(f"Prompt: {prompt}")

        # Define the chain
        chain = prompt | self.llm | self.output_parser

        langfuse_handler = CallbackHandler()

        # logging.info(f"User message: {user_msg}")

        # logging.info(f"Prompt template: {self.prompt}")
        # Generate questions with an empty question request

        questions_set = chain.invoke(
            {"input": [""]},
            config={
                "configurable": {"session_id": self.session_id},
                "callbacks": [langfuse_handler],
                "run_name": "assignment_questions",
                "tags": [
                    "assignment_questions",
                    settings.OPENAI_MODEL,
                ],
                "metadata": {
                    "langfuse_session_id": str(self.session_id),
                },
            },
        )

        return questions_set.questions, questions_set.metadata
