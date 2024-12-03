from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langfuse.callback import CallbackHandler
from typing import AsyncGenerator

from app.prompt import ClinicalPracticePrompt
from app.core.config import settings


class ChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: list[BaseMessage] = []

    def add_messages(self, messages):
        """Add multiple messages from the database to the chat history."""
        for message in messages:
            # Assuming message is a SQLAlchemy model with content and role attributes
            role = message.role if hasattr(message, "role") else message["role"]
            content = (
                message.content if hasattr(message, "content") else message["content"]
            )

            if role == "doctor":
                self.messages.append(HumanMessage(content=content))
            else:
                self.messages.append(AIMessage(content=content))

    def clear(self):
        """Clear the chat history."""
        self.messages.clear()

    def add_message(self, message: BaseMessage):
        """Add a single message to the history."""
        self.messages.append(message)

    def get_messages(self) -> list[BaseMessage]:
        """Return the list of messages."""
        return self.messages


class ClinicalPracticeLLM:
    def __init__(self, session_id, scenario, scenario_examination_findings):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=0,
            streaming=True,
            max_tokens=100,
        )
        self.thread_id = session_id
        self.memory = ChatMessageHistory(session_id)
        self.prompt = ClinicalPracticePrompt().create_prompt(
            scenario, scenario_examination_findings
        )
        self.chain = self.prompt | self.llm

    async def generate_response_stream(
        self, question: str, thread_messages: list
    ) -> AsyncGenerator[str, None]:
        try:
            if thread_messages:
                self.memory.add_messages(thread_messages)

            def get_session_history() -> ChatMessageHistory:
                return self.memory

            with_history = RunnableWithMessageHistory(
                self.chain,
                get_session_history,
                input_messages_key="messages",
                history_messages_key="history",
            )

            langfuse_handler = CallbackHandler()

            async for chunk in with_history.astream(
                {"messages": [HumanMessage(content=question)]},
                config={
                    "configurable": {"session_id": self.thread_id},
                    "callbacks": [langfuse_handler],
                    "run_name": "chat",
                    "tags": [
                        "chat",
                        settings.OPENAI_MODEL,
                    ],
                    "metadata": {
                        "langfuse_session_id": str(self.thread_id),
                    },
                },
            ):
                if hasattr(chunk, "content"):
                    yield chunk.content
                else:
                    yield str(chunk)

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            raise
