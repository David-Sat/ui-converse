import json
from langchain.schema import StrOutputParser, ChatMessage
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from typing import Dict, Any, Callable
from pathlib import Path

class Chat:
    def __init__(self, openai_api_key, model="gpt-3.5-turbo-1106", streaming=True):


        self.openai_api_key = openai_api_key
        self.model = ChatOpenAI(openai_api_key=self.openai_api_key, model_name=model, streaming=streaming)
        self.messages = []
        self.config = self.load_config()
        self.system_prompt = self.config["system_prompt"]
        self.few_shot_examples = self.config["few_shot_examples"]

    def load_config(self):
        config_path = Path(__file__).resolve().parent.parent / 'configs' / 'config.json'
        with config_path.open('r', encoding='utf-8') as f:
            config = json.load(f)
        return config


    def __call__(self, messages, stream_handler: Callable) -> str:
        prompt = self._get_prompt(messages)
        response = self._get_response(prompt, stream_handler)
        return response


    def _get_prompt(self, messages):
        example_prompt = ChatPromptTemplate.from_messages(
                [
                    ("human", "{input}"), 
                    ("ai", "{output}"),
                ]
            )

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=self.few_shot_examples,
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                few_shot_prompt,
                ("human", "What is the ideal electric car for me?")
            ] 
        )

        

        return prompt

    def _get_response(self, prompt, stream_handler: Callable):
        print(prompt)
        chain = (
            prompt
            | self.model
            | StrOutputParser()
        )

        config = {"callbacks": [stream_handler]}
        response = chain.invoke(input={}, config=config)
        self.messages.append(ChatMessage(role="assistant", content=response))
        return response


