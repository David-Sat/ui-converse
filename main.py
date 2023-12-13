import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from llm_utils.stream_handler import StreamHandler
from streamlit_utils.ui_creator import display_ui_from_response
from llm_utils.chat import Chat


def get_openai_api_key():
    if "openai_api_key" not in st.session_state:
        if "openai_api_key" in st.secrets:
            st.session_state["openai_api_key"] = st.secrets.openai_api_key
        else:
            st.session_state["openai_api_key"] = st.sidebar.text_input("OpenAI API Key", type="password")
    if not st.session_state["openai_api_key"]:
        st.info("Enter an OpenAI API Key to continue")
        st.stop()

get_openai_api_key()

chat_instance = Chat(st.session_state.openai_api_key, "gpt-3.5-turbo", streaming=True)

if "messages" not in st.session_state:
    #st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]
    st.session_state["messages"] = []

chat_container = st.container()

for index, msg in enumerate(st.session_state.messages):
    if msg.role == "assistant":
        with chat_container.chat_message("assistant"):
            display_ui_from_response(msg.content, index)
    else:
        chat_container.chat_message(msg.role).write(msg.content)

user_input = chat_container.text_input("Your message", key="user_input")

col1, col2 = chat_container.columns(2)
with col2:
    if st.button("Clear Chat"):
        st.session_state.messages = []

with col1:
    if st.button("Submit", type="primary"):
        if user_input:
            st.session_state.messages.append(ChatMessage(role="user", content=user_input))

        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            response = chat_instance(st.session_state.messages, stream_handler)
            st.session_state.messages.append(ChatMessage(role="assistant", content=response))