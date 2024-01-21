

def prompt_assembly(user_ui_inputs: dict, user_text_input):
    prompt = ""
    for key, value in user_ui_inputs.items():
        prompt += f"{key}: {value}\n"

    if user_text_input:
        prompt += f"{user_text_input}; "

    return prompt