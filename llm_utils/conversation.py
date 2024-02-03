"""Defines the Conversation class for managing chat interactions using different language models."""
import json
from typing import Callable
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from llm_utils.agents import ConversationalAgent, UIAgent


class Conversation:
    """Initializes conversation and UI agents with specified models and API keys."""

    def __init__(
            self,
            api_keys: dict,
            model_name_conv="gemini-pro",
            model_name_ui="gemini-pro") -> None:
        """Initialize conversation and UI agents using given API keys and model names."""
        self.api_keys = api_keys

        conv_model = self.create_model(model_name_conv, streaming=True)
        ui_model = self.create_model(model_name_ui, streaming=False)

        self.conversational_agent = ConversationalAgent(conv_model)
        self.ui_agent = UIAgent(ui_model)

    def __call__(self, message: HumanMessage, stream_handler: Callable) -> str:
        """Process a chat message through the conversational agent and generate UI response."""
        textual_response = self.conversational_agent(message, stream_handler)
        json_response = self.ui_agent(textual_response)

        json_response["text"] = textual_response.split("␃")[0]
        json_response = json.dumps(json_response)

        return textual_response, json_response

    def update_agents(self, model_name_conv: str, model_name_ui: str):
        """Update conversational and UI agents with new models."""
        print(
            f"Updating agents with models {model_name_conv} and {model_name_ui}")
        conv_agent_model = self.create_model(
            model_name=model_name_conv, streaming=True)
        ui_agent_model = self.create_model(
            model_name=model_name_ui, streaming=False)

        self.conversational_agent.update_model(conv_agent_model)
        self.ui_agent.update_model(ui_agent_model)

    def create_model(self, model_name: str, streaming=False):
        """Create a model instance based on model name and streaming capability."""
        if model_name in ("gpt-3.5-turbo-1106", "gpt-4-turbo-preview"):
            api_key = self.api_keys["openai"]
            return ChatOpenAI(openai_api_key=api_key, model_name=model_name, streaming=streaming)

        if model_name == "gemini-pro":
            api_key = self.api_keys["google"]
            return ChatGoogleGenerativeAI(
                model="gemini-pro",
                stream=streaming,
                convert_system_message_to_human=True
            )
        return None
