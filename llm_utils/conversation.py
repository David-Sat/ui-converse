
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from typing import Callable
from llm_utils.agents import ConversationalAgent, UIAgent


class Conversation:
    def __init__(self, api_key_conv, api_key_ui, model_name_conv="gpt-3.5-turbo-1106", model_name_ui="gpt-3.5-turbo-1106") -> None:
        self.api_key_conv = api_key_conv
        self.api_key_ui = api_key_ui
        
        self.conversational_agent = ConversationalAgent(ChatOpenAI(openai_api_key=self.api_key_conv, model_name=model_name_conv, streaming=True))
        self.ui_agent = UIAgent(ChatOpenAI(openai_api_key=self.api_key_ui, model_name=model_name_ui))


    def __call__(self, message: ChatMessage, stream_handler: Callable) -> str:
        textual_response = self.conversational_agent(message, stream_handler)
        ui_response = self.ui_agent(textual_response)

        json_response = json.loads(ui_response)
        json_response["text"] = textual_response.split("␃")[0]
        json_response = json.dumps(json_response)

        return textual_response, json_response