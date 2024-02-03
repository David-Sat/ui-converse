"""assemble prompt string based on user input"""


def prompt_assembly(user_ui_inputs: dict, user_text_input: str) -> str:
    """
    Assembles a prompt string based on the user's UI inputs and text input.

    Args:
        user_ui_inputs (dict): A dictionary containing the user's UI inputs.
        user_text_input: The user's text input.

    Returns:
        str: The assembled prompt string.
    """
    prompt = ""
    for key, value in user_ui_inputs.items():
        if value != "None":
            prompt += f"{key}: {value};\n"

    if user_text_input:
        prompt += f"{user_text_input}; "

    return prompt
