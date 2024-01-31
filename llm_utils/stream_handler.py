from langchain.callbacks.base import BaseCallbackHandler
from typing import Any, Dict, List

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

    def get_accumulated_response(self):
        return self.text


class DebugHandler(BaseCallbackHandler):
    def __init__(self, initial_text=""):
        pass

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Print out the prompts."""
        print(prompts)



class StreamUntilSpecialTokenHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text="", special_token="␃"):
        self.container = container
        self.text = initial_text
        self.special_token = special_token
        self.special_token_reached = False

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.special_token_reached:
            return
        if token.strip() == self.special_token:
            self.special_token_reached = True
            return
        self.text += token
        self.container.markdown(self.text)

    def get_accumulated_response(self):
        return self.text
