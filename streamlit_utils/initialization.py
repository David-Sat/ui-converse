import streamlit as st


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
    if "messages" not in st.session_state:
        #st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]
        st.session_state["messages"] = []
    if "user_inputs" not in st.session_state:
        st.session_state["user_inputs"] = {}

    if 'input_text' not in st.session_state:
        st.session_state.input_text = "I want to buy an electric car"