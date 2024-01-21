import json
from langchain.schema import StrOutputParser, ChatMessage
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from llm_utils.config_loader import load_few_shot_examples, load_config

example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"), 
                ("ai", "{output}"),
            ]
        )

class Reasoner:
    def __init__(self, openai_api_key, model="gpt-3.5-turbo-1106", streaming=True):
        self.openai_api_key = openai_api_key
        self.model = ChatOpenAI(openai_api_key=self.openai_api_key, model_name=model, streaming=streaming)
        self.memory = []
        self.config = load_config()
        self.system_prompt = self.config["reasoning_prompt"]
        self.few_shot_examples = load_few_shot_examples('configs/reasoning_examples.json')


    def __call__(self, message: ChatMessage) -> str:
        self.memory.append(message)
        prompt = self._get_prompt()
        response = self._get_response(prompt)
        return response


    def _get_prompt(self):
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=self.few_shot_examples,
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                few_shot_prompt,
            ]
            + self.memory
        )

        print("memory: ", self.memory)

        return prompt

    def _get_response(self, prompt):
        chain = (
            prompt
            | self.model
            | StrOutputParser()
        )

        response = chain.invoke(input={})
        self.memory.append(ChatMessage(role="assistant", content=response))
        return response

