import streamlit as st
from llm_utils.conversation import Conversation

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

    if "conversation" not in st.session_state:
        st.session_state["conversation"] = Conversation(st.session_state.openai_api_key, st.session_state.openai_api_key)


    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "conv_history" not in st.session_state:
        st.session_state["conv_history"] = []
    if "user_inputs" not in st.session_state:
        st.session_state["user_inputs"] = {}

    if 'input_text' not in st.session_state:
        st.session_state.input_text = "I want to buy an electric car"