import streamlit as st
from llm_utils.reasoning import Reasoner
from llm_utils.acting import Actor

def get_openai_api_key():
    if "openai_api_key" not in st.session_state:
        if "openai_api_key" in st.secrets:
            st.session_state["openai_api_key"] = st.secrets.openai_api_key
        else:
            st.session_state["openai_api_key"] = st.sidebar.text_input("OpenAI API Key", type="password")
    if not st.session_state["openai_api_key"]:
        st.info("Enter an OpenAI API Key to continue")
        st.stop()

def initialize_session():
    get_openai_api_key()
    
    """Set default values in the session state if not already initialized."""

    if "reasoner" not in st.session_state:
        st.session_state["reasoner"] = Reasoner(st.session_state.openai_api_key, "gpt-3.5-turbo", streaming=True)

    if "actor" not in st.session_state:
        st.session_state["actor"] = Actor(st.session_state.openai_api_key, "gpt-3.5-turbo", streaming=True)

    if "messages" not in st.session_state:
        #st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]
        st.session_state["messages"] = []
    if "history" not in st.session_state:
        st.session_state["history"] = []
    if "user_inputs" not in st.session_state:
        st.session_state["user_inputs"] = {}

    if 'input_text' not in st.session_state:
        st.session_state.input_text = "I want to buy an electric car"