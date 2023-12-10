from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        self.in_ui_section = False

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if token == "<ui>":
            self.in_ui_section = True
        elif token == "</ui>":
            self.in_ui_section = False
            return  # Skip appending the </ui> tag

        if not self.in_ui_section:
            self.text += token
            self.container.markdown(self.text)
