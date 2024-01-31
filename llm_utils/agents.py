import json
from llm_utils.config_loader import load_few_shot_examples, load_config
from langchain.schema import StrOutputParser, ChatMessage
from langchain.chat_models.base import BaseChatModel
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llm_utils.pydantic_models import Output
from typing import Any, Dict, List, Callable

from langchain.callbacks.base import BaseCallbackHandler


class DebugHandler(BaseCallbackHandler):
    def __init__(self, initial_text=""):
        pass

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Print out the prompts."""
        print(prompts)


class Agent:
    def __init__(self, model: BaseChatModel):
        self.model = model
        self.config = load_config()

        self.example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"), 
                ("ai", "{output}"),
            ]
        )


class ConversationalAgent(Agent):
    def __init__(self, model: BaseChatModel):
        super().__init__(model)
        self.memory = []
        self.system_prompt = self.config["conversational_prompt"]
        self.few_shot_examples = load_few_shot_examples('configs/reasoning_examples.json')


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
    def __init__(self, model: BaseChatModel):
        super().__init__(model)
        self.system_prompt = self.config["ui_prompt"]


    def __call__(self, message) -> str:
        parser = PydanticOutputParser(pydantic_object=Output)

        prompt = PromptTemplate(
            template="{system_prompt}\n{format_instructions}\n{message}",
            input_variables=["message"],
            partial_variables={"system_prompt": self.system_prompt, "format_instructions": parser.get_format_instructions()},
        )
        
        chain = (
            prompt 
            | self.model 
            | parser
        )

        handler = DebugHandler()
        config = {"callbacks": [handler]}

        try:
            validated_data = chain.invoke(input={"message": message}, config=config)
            return json.dumps(validated_data.dict())
        except Exception as e:
            return f"Error: {e}"

