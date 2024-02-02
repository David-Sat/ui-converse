"""Module for handling streaming and debugging of llm outputs with custom callback handlers."""
from typing import Any, Dict, List
from langchain.callbacks.base import BaseCallbackHandler


class StreamHandler(BaseCallbackHandler):
    """Handles real-time streaming of LLM output tokens to a Streamlit container."""

    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Streams tokens to the container."""
        self.text += token
        self.container.markdown(self.text)

    def get_accumulated_response(self):
        """Returns the accumulated text from LLM output."""
        return self.text


class DebugHandler(BaseCallbackHandler):
    """Debug handler for printing out the prompts used in LLM requests."""

    def __init__(self, initial_text=""):
        pass

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Print out the prompts."""
        # print(prompts)


class StreamUntilSpecialTokenHandler(BaseCallbackHandler):
    """Handles streaming LLM outputs to a container until a special token is encountered."""

    def __init__(self, container, initial_text="", special_token="␃"):
        self.container = container
        self.text = initial_text
        self.special_token = special_token
        self.special_token_reached = False

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Streams tokens to the container, stopping if the special token is reached."""
        if self.special_token_reached:
            return
        if token.strip() == self.special_token:
            self.special_token_reached = True
            return
        self.text += token
        self.container.markdown(self.text)

    def get_accumulated_response(self):
        """Returns the accumulated text from LLM output."""
        return self.text
