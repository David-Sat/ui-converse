"""Initialization of the session state and models."""
import streamlit as st
from llm_utils.conversation import Conversation


def get_api_key(provider):
    """Get the API key for the specified provider."""
    api_key_name = provider + "_api_key"
    if api_key_name not in st.session_state:
        if api_key_name in st.secrets:
            return st.secrets[api_key_name]
        else:
            return st.sidebar.text_input(f"{api_key_name} API Key", type="password")


def initialize_models():
    """Initialize the models and API keys."""
    st.session_state["models_initialized"] = True
    st.session_state["supported_providers"] = ["openai", "google"]

    st.session_state["supp_models_conversation"] = [
        "gpt-3.5-turbo-1106",
        "gpt-4-turbo-preview",
        "gemini-pro"
    ]
    st.session_state["supp_models_ui"] = [
        "gpt-3.5-turbo-1106",
        "gpt-4-turbo-preview",
        "gemini-pro"
    ]

    st.session_state["sel_model_conversation"] = st.session_state["supp_models_conversation"][2]
    st.session_state["sel_model_ui"] = st.session_state["supp_models_ui"][2]


def initialize_session():
    """Set default values in the session state if not already initialized."""

    if "models_initialized" not in st.session_state:
        initialize_models()

    api_keys = {}
    for provider in st.session_state["supported_providers"]:
        api_keys[provider] = get_api_key(provider)

    if "conversation" not in st.session_state:
        st.session_state["conversation"] = Conversation(api_keys)

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "conv_history" not in st.session_state:
        st.session_state["conv_history"] = []
    if "user_inputs" not in st.session_state:
        st.session_state["user_inputs"] = {}

    if 'input_text' not in st.session_state:
        st.session_state.input_text = "I want to buy an electric car"
