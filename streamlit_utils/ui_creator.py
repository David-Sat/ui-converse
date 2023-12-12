import streamlit as st
import xml.etree.ElementTree as ET
from io import StringIO

def display_ui_from_response(response, message_index):
    markdown_part, ui_part = extract_parts(response)
    display_markdown(markdown_part)
    if ui_part:
        display_ui_elements(ui_part, message_index)

def extract_parts(response):
    """Extracts Markdown and UI parts from the response."""
    if "<ui>" in response:
        markdown_part, ui_part = response.split("<ui>", 1)
        ui_part = ui_part.split("</ui>", 1)[0]
    else:
        markdown_part, ui_part = response, ""
    return markdown_part, ui_part


def display_markdown(markdown_part):
    """Displays the Markdown part of the response."""
    st.markdown(markdown_part)

def display_ui_elements(ui_part, message_index):
    """Parses and displays UI elements from the UI part of the response."""
    ui_xml = f"<root>{ui_part}</root>"
    root = ET.parse(StringIO(ui_xml)).getroot()
    for index, element in enumerate(root):
        display_ui_element(element, message_index, index)

def display_ui_element(element, message_index, index):
    """Displays a single UI element based on its tag and attributes."""
    label = element.attrib.get('label', '')
    key = f"{element.tag}_{label}_{message_index}_{index}"

    if element.tag == 'slider':
        display_slider(element, label, key)
    elif element.tag == 'multiSelect':
        display_multiselect(element, label, key)
    elif element.tag == 'textInput':
        display_text_input(label, key)



def display_slider(element, label, key):
    """Displays a slider UI element."""
    min_value = int(element.attrib.get('min_value', 0))
    max_value = int(element.attrib.get('max_value', 100))
    slider_value = st.slider(label, min_value, max_value, key=key)
    st.session_state.user_inputs[label] = slider_value

def display_multiselect(element, label, key):
    """Displays a multi-select UI element."""
    options = [opt.text for opt in element]
    st.multiselect(label, options, key=key)

def display_text_input(label, key):
    """Displays a text input UI element."""
    st.text_input(label, key=key)
