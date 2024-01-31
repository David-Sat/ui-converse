import streamlit as st
from langchain.schema import ChatMessage
from llm_utils.stream_handler import StreamUntilSpecialTokenHandler
from streamlit_utils.ui_creator import display_ui_from_response
from streamlit_utils.initialization import initialize_session
from llm_utils.conversation import Conversation
from llm_utils.prompt_assembly import prompt_assembly

from typing import Optional


def get_conversation() -> Optional[Conversation]:
    return st.session_state.get("conversation", None)

def handle_submission():
    user_input = st.session_state.input_text
    user_prompt = prompt_assembly(st.session_state.user_inputs, user_input)
    user_message = ChatMessage(role="user", content=user_prompt)
    st.session_state.messages.append(user_message)
    st.session_state.conv_history.append(user_message)

    conversation_instance = get_conversation()

    with st.chat_message("assistant"):
        stream_handler = StreamUntilSpecialTokenHandler(st.empty())

        textual_response, json_response = conversation_instance(user_message, stream_handler)

        st.session_state.conv_history.append(ChatMessage(role="assistant", content=textual_response))
        st.session_state.conv_history.append(ChatMessage(role="assistant", content=json_response))
        st.session_state.messages.append(ChatMessage(role="assistant", content=json_response))


    # Reset the input field
    st.session_state.input_text = ""

    # Rerun the Streamlit app to update the UI
    st.session_state.user_inputs = {}
    st.rerun()


def main():
    # Initialize session state and OpenAI API key
    initialize_session()

    with st.expander("Debug Info"):
        st.write(st.session_state.conv_history)

    chat_container = st.container()

    for index, msg in enumerate(st.session_state.messages):
        if msg.role == "assistant":
            with chat_container.chat_message("assistant"):
                display_ui_from_response(msg.content, index, len(st.session_state.messages)-1)
        else:
            chat_container.chat_message(msg.role).write(msg.content)


    st.session_state.input_text = chat_container.text_input(
        "Your prompt",
        value=st.session_state.input_text)

    col1, col2 = chat_container.columns(2)

    if col2.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()


    if col1.button("Submit", type="primary"):
        handle_submission()


if __name__ == "__main__":
    main()
