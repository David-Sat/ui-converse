"""Streamlit app module for interactive chat management and display."""
from typing import Optional
import streamlit as st
from langchain.schema import ChatMessage
from functools import wraps
from streamlit_utils.ui_creator import display_ui_from_response
from streamlit_utils.initialization import initialize_session
from llm_utils.stream_handler import StreamUntilSpecialTokenHandler
from llm_utils.conversation import Conversation
from llm_utils.prompt_assembly import prompt_assembly


def show_spinner(func):
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        with st.spinner('Updating models...'):
            return func(*args, **kwargs)
    return wrapper_function


def get_conversation() -> Optional[Conversation]:
    """Retrieve the current conversation instance from Streamlit's session state."""
    return st.session_state.get("conversation", None)


def handle_submission():
    """Process and submit user input, updating conversation history."""
    user_input = st.session_state.input_text
    user_prompt = prompt_assembly(st.session_state.user_inputs, user_input)
    user_message = ChatMessage(role="user", content=user_prompt)
    st.session_state.messages.append(user_message)
    st.session_state.conv_history.append(user_message)

    conversation_instance = get_conversation()

    with st.chat_message("assistant"):
        stream_handler = StreamUntilSpecialTokenHandler(st.empty())

        textual_response, json_response = conversation_instance(
            user_message, stream_handler)

        st.session_state.conv_history.append(ChatMessage(
            role="assistant", content=textual_response))
        st.session_state.conv_history.append(
            ChatMessage(role="assistant", content=json_response))
        st.session_state.messages.append(ChatMessage(
            role="assistant", content=json_response))

    st.session_state.input_text = ""

    st.session_state.user_inputs = {}
    st.rerun()


def handle_sidebar():
    """Manage sidebar interactions for model selection and updates in the Streamlit app."""
    with st.sidebar:
        st.subheader("Conversation Agent")
        conv_selection = model_selection("Conversation")
        st.subheader("UI Agent")
        ui_selection = model_selection("UI")

        if st.button("Update Agents"):
            update_conversation(conv_selection, ui_selection)


def update_conversation(conv_selection, ui_selection):
    """Update the conversation instance with new models for conversation and UI agents."""
    conversation_instance = get_conversation()
    conversation_instance.update_agents(conv_selection, ui_selection)


def model_selection(agent):
    """Display and handle model selection radio button."""
    label = f"{agent} Model"
    options = st.session_state[f"supp_models_{agent.lower()}"]
    index = options.index(st.session_state[f"sel_model_{agent.lower()}"])

    selection = st.radio(label, options, index)
    st.session_state[f"sel_model_{agent.lower()}"] = selection

    return selection


def main():
    """Main function to initialize and run the Streamlit application."""
    initialize_session()
    handle_sidebar()

    with st.expander("Debug Info"):
        st.write(st.session_state.conv_history)

    chat_container = st.container()

    for index, msg in enumerate(st.session_state.messages):
        if msg.role == "assistant":
            with chat_container.chat_message("assistant"):
                display_ui_from_response(
                    msg.content, index, len(st.session_state.messages)-1)
        else:
            chat_container.chat_message(msg.role).write(msg.content)

    st.session_state.input_text = chat_container.text_input(
        "Your prompt",
        value=st.session_state.input_text)

    col1, col2 = chat_container.columns(2)

    if col2.button("Restart Session"):
        st.session_state.messages = []
        st.rerun()

    if col1.button("Submit", type="primary"):
        handle_submission()


if __name__ == "__main__":
    main()
