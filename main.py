import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from llm_utils.StreamHandler import StreamHandler
from llm_utils.ui_agent import get_mock_response, UIAgent
from streamlit_utils.ui_creator import display_ui_from_response


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

ui_agent = UIAgent(st.session_state.openai_api_key, "gpt-3.5-turbo")

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

chat = st.container()

for index, msg in enumerate(st.session_state.messages):
    if msg.role == "assistant":
        with chat.chat_message("assistant"):
            display_ui_from_response(msg.content, index)
    else:
        chat.chat_message(msg.role).write(msg.content)

col1, col2 = chat.columns(2)
with col2:
    if st.button("Clear Chat"):
        st.session_state.messages = []

with col1:
    if st.button("Submit", type="primary"):

        # TODO: Submit chat to backend
        # st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        # st.chat_message("user").write(prompt)
        pass

        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            response = ui_agent.ask(st.session_state.messages, stream_handler)
            llm = ChatOpenAI(openai_api_key=st.session_state.openai_api_key, streaming=True, callbacks=[stream_handler])
            #response = llm(st.session_state.messages)
            #st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))
            #response = get_mock_response()
            st.session_state.messages.append(ChatMessage(role="assistant", content=response))