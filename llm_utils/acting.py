import json
from langchain.schema import StrOutputParser, ChatMessage
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from typing import Dict, Any, Callable
from llm_utils.config_loader import load_few_shot_examples, load_few_shot_json_examples, load_config
from llm_utils.pydantic_models import Output
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate



example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"), 
                ("ai", "{output}"),
            ]
        )

class Actor:
    def __init__(self, openai_api_key, model="gpt-3.5-turbo-1106", streaming=True):
        self.openai_api_key = openai_api_key
        self.model = ChatOpenAI(openai_api_key=self.openai_api_key, model_name=model, streaming=streaming)
        self.messages = []
        self.config = load_config()
        self.system_prompt = self.config["acting_prompt"]
        self.few_shot_acting_examples = load_few_shot_json_examples('configs/acting_examples.json')
        self.few_shot_reasoning_examples = load_few_shot_examples('configs/reasoning_examples.json')


    def __call__(self, message, stream_handler: Callable) -> str:
        
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

        config = {"callbacks": [stream_handler]}

        try:
            validated_data = chain.invoke(input={"message": message}, config=config)
            return json.dumps(validated_data.dict())
        except Exception as e:
            return f"Error: {e}"



