from langchain.schema import StrOutputParser, ChatMessage
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.chat_models import ChatOpenAI

from typing import Dict, Any, Callable
from pathlib import Path
import json

example_prompt = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"),
                ("ai", "{output}"),
            ]
        )

class UIAgent:
    def __init__(self, openai_api_key, model_name):
        self.model = ChatOpenAI(openai_api_key=openai_api_key, model_name=model_name, streaming=True)
        config = self.load_config()
        self.system_prompt = config["system_prompt"]
        self.few_shot_examples = config["few_shot_examples"]
        
    def load_config(self):
        config_path = Path(__file__).resolve().parent.parent / 'configs' / 'config.json'
        with config_path.open('r', encoding='utf-8') as f:
            config = json.load(f)
        return config


    def ask(self, conversation, stream_handler: Callable) -> str:
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=self.few_shot_examples,
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                few_shot_prompt
            ] + conversation
        )
        
        chain = (
            prompt
            | self.model
            | StrOutputParser()
        )

        config = {
            "callbacks": [stream_handler]
        }

        print(prompt)
        return chain.invoke(input={}, config=config)



def get_mock_response():
    response = """
### Discover Your Ideal BMW Model 🏎️

When looking to buy a BMW and finding out which model aligns with your lifestyle, think about your daily activities, driving habits, and specific needs from a vehicle.

<ui>
<multiSelect label="Select Your Lifestyle">
<option>Adventurous</option>
<option>Family-Oriented</option>
<option>Luxury Seeker</option>
<option>Eco-Conscious</option>
</multiSelect>

<slider label="Set Your Budget" min_value="30000" max_value="150000" />

<multiSelect label="Select Additional Features">
<option>Sunroof</option>
<option>Leather Seats</option>
<option>Sound System</option>
<option>Sport Package</option>
</multiSelect>

<textInput label="Specify Additional Car Features" />
</ui>
    """
    return response
