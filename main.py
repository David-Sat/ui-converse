import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from llm_utils.stream_handler import StreamHandler
from streamlit_utils.ui_creator import display_ui_from_response
from streamlit_utils.initialization import initialize_session
from llm_utils.chat import Chat
from llm_utils.prompt_assembly import prompt_assembly


def main():
    # Initialize session state and OpenAI API key
    initialize_session()

    st.write(st.session_state.messages)

    chat_instance = Chat(st.session_state.openai_api_key, "gpt-3.5-turbo", streaming=True)

    chat_container = st.container()

    for index, msg in enumerate(st.session_state.messages):
        if msg.role == "assistant":
            with chat_container.chat_message("assistant"):
                display_ui_from_response(msg.content, index)
        else:
            chat_container.chat_message(msg.role).write(msg.content)

    if 'input_text' not in st.session_state:
        st.session_state.input_text = "I want to buy an electric car"

    user_input = chat_container.text_input("Your message", value=st.session_state.input_text)

    col1, col2 = chat_container.columns(2)
    with col2:
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    with col1:
        if st.button("Submit", type="primary"):
            print("user inputs:", st.session_state.user_inputs)
            user_prompt = prompt_assembly(st.session_state.user_inputs, user_input)
            st.session_state.messages.append(ChatMessage(role="user", content=user_prompt))
            st.session_state.input_text = ""

            with st.chat_message("assistant"):
                stream_handler = StreamHandler(st.empty())
                response = chat_instance(st.session_state.messages, stream_handler)
                st.session_state.messages.append(ChatMessage(role="assistant", content=response))
                st.rerun()




if __name__ == "__main__":
    main()
