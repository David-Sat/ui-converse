import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from llm_utils.stream_handler import StreamHandler
from streamlit_utils.ui_creator import display_ui_from_response
from streamlit_utils.initialization import initialize_session
from llm_utils.chat import Chat
from llm_utils.prompt_assembly import prompt_assembly



initialize_session()

chat_instance = Chat(st.session_state.openai_api_key, "gpt-3.5-turbo", streaming=True)


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
        print("user inputs:", st.session_state.user_inputs)
        user_prompt = prompt_assembly(st.session_state.user_inputs, user_input)
        st.session_state.messages.append(ChatMessage(role="user", content=user_prompt))

        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            response = chat_instance(st.session_state.messages, stream_handler)
            st.session_state.messages.append(ChatMessage(role="assistant", content=response))