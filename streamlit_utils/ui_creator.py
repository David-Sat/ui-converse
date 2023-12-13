import streamlit as st
import json

def display_ui_from_response(response, message_index):
    data = json.loads(response)
    try:
        data = json.loads(response)
        print("Parsed JSON:", data)
        display_markdown(data["title"])
        display_markdown(data["full_answer"])
        if "ui_elements" in data:
            for index, element in enumerate(data["ui_elements"]):
                display_ui_element(element, message_index, index)
    except json.JSONDecodeError:
        display_markdown(response)


def display_markdown(markdown_part):
    """Displays the Markdown part of the response."""
    st.markdown(markdown_part)

def display_ui_element(element, message_index, index):
    """Displays a single UI element based on its type and attributes."""
    label = element.get('label', '')
    key = f"{element['type']}_{label}_{message_index}_{index}"

    print(f"Displaying UI element: {element['type']} - {element.get('label', '')}")

    if element['type'] == 'Slider':
        display_slider(element, label, key)
    elif element['type'] == 'RadioButtons':
        display_radio_buttons(element, label, key)
    elif element['type'] == 'MultiSelect':
        display_multiselect(element, label, key)
    elif element['type'] == 'TextInput':
        display_text_input(label, key)

def display_slider(element, label, key):
    """Displays a slider UI element."""
    min_value, max_value = element.get('range', [0, 100])
    slider_value = st.slider(label, min_value, max_value, key=key)
    st.session_state.user_inputs[label] = slider_value

def display_radio_buttons(element, label, key):
    """Displays radio buttons UI element."""
    options = element.get('options', [])
    selected_option = st.radio(label, options, key=key)
    st.session_state.user_inputs[label] = selected_option

def display_multiselect(element, label, key):
    """Displays a multi-select UI element."""
    options = element.get('options', [])
    selected_options = st.multiselect(label, options, key=key)
    st.session_state.user_inputs[label] = selected_options

def display_text_input(label, key):
    """Displays a text input UI element."""
    text_value = st.text_input(label, key=key)
    st.session_state.user_inputs[label] = text_value
