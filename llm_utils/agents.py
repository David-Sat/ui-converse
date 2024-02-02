"""Module for defining agents that interact with LLMs for conversational and UI responses."""
from typing import Callable
import traceback
from langchain.schema import StrOutputParser, ChatMessage
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import ValidationError
from llm_utils.pydantic_models import Output
from llm_utils.config_loader import load_few_shot_examples, load_config
from llm_utils.stream_handler import DebugHandler


class Agent:
    """Base class for agents interacting with LLMs."""

    def __init__(self, model):
        self.model = model
        self.config = load_config()

        self.example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"),
                ("ai", "{output}"),
            ]
        )

    def update_model(self, model):
        """Updates the agent's model."""
        self.model = model

    def get_model(self):
        """Returns the agent's model."""
        return self.model


class ConversationalAgent(Agent):
    """Agent for handling conversations."""

    def __init__(self, model):
        super().__init__(model)
        self.memory = []
        self.system_prompt = self.config["conversational_prompt"]
        self.few_shot_examples = load_few_shot_examples(
            'configs/reasoning_examples.json')

    def __call__(self, message: ChatMessage, stream_handler: Callable) -> str:
        self.memory.append(message)

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=self.example_prompt,
            examples=self.few_shot_examples,
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                few_shot_prompt,
            ]
            + self.memory
        )

        chain = (
            prompt
            | self.model
            | StrOutputParser()
        )

        config = {"callbacks": [stream_handler]}
        response = chain.invoke(input={}, config=config)
        self.memory.append(ChatMessage(role="assistant", content=response))
        return response


class UIAgent(Agent):
    """Agent for generating UI responses based on model outputs."""

    def __init__(self, model):
        super().__init__(model)
        self.system_prompt = self.config["ui_prompt"]

    def __call__(self, message) -> str:
        parser = PydanticOutputParser(pydantic_object=Output)

        prompt = PromptTemplate(
            template="{system_prompt}\n{format_instructions}\n{message}",
            input_variables=["message"],
            partial_variables={"system_prompt": self.system_prompt,
                               "format_instructions": parser.get_format_instructions()},
        )

        chain = (
            prompt
            | self.model
            | parser
        )

        handler = DebugHandler()
        config = {"callbacks": [handler]}

        retries = 3  # Number of retries
        for attempt in range(retries):
            try:
                validated_data = chain.invoke(
                    input={"message": message}, config=config)
                return validated_data.dict()
            except ValidationError as e:
                print(f"Validation error on attempt {attempt+1}: {e}")
                if attempt == retries - 1:
                    return None
                print("Retrying...")
            except Exception as e:
                print(f"Unexpected error: {traceback.format_exc()} - {e}")
                return None
