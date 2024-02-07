# UIConverse
UIConverse transforms the way users interact with LLMs by introducing a user-friendly interface that eliminates the need for complex typing and prompt crafting. This innovative system leverages a dual-agent architecture to offer initial responses and generate on-the-fly UIs, such as sliders and checkboxes, for intuitive user refinement. It addresses common issues like inefficient interactions and underutilization of LLM capabilities making LLMs more accessible and tailored to individual user needs.

UIConverse is currently deployed [here](https://uiconverse.streamlit.app/).

## Problem Statement
### Challenges with Current LLM Interactions

The current landscape of interacting with large language models poses several challenges that hinder user experience and limit the technology's potential:

- **Clunky and Inefficient Interactions:** Interacting with LLMs is often awkward and inefficient, requiring multiple steps and long texts to achieve simple tasks.
- **Lack of Awareness:** There is a significant gap in users' understanding of what LLMs are capable of, leading to underutilization of their functionalities.
- **Security Risks:** The ability to insert text into LLMs opens up avenues for prompt injections by malicious actors, posing a threat to security.
- **Overly Broad Capabilities:** While LLMs can perform a wide range of tasks, not all these capabilities lead to meaningful or useful outcomes for the user, suggesting a need for more focused and reasonable options.

### Need for Improved User Experience

To address these challenges, there's a pressing need for a system that not only streamlines the interaction process but also enhances security and guides users toward a more productive use of LLM capabilities.

## Solution Overview

### Introducing UIConverse

UIConverse is designed to transform how users interact with LLMs. This system empowers users to obtain information on various topics without the traditional back-and-forth chatting, making the experience more efficient and user-friendly.

### How It Works

- **Initial User Request:** Users start by typing their request into the system.
- **Dynamic Response System:** The system provides an initial answer followed by a custom UI created on-the-fly, tailored to the user's needs.
- **Custom UI Interaction:** Users interact with the UI — featuring radio buttons, sliders, multiselects, checkboxes, etc. — instead of typing responses. This UI simplifies the process of refining their request.
- **Prompt Conversion and Continuation:** User inputs from the UI are converted into prompts and sent back to the system, allowing the conversation to continue seamlessly until the user's goal is achieved.


Sequence Diagram

![Sequence Diagram](https://github.com/David-Sat/ui-converse/blob/main/sequence_diagram.png)

Conversation Flow Diagram

![Conversation Flow](https://github.com/David-Sat/ui-converse/blob/main/conversation_flow.drawio.png)

### Architectural Highlights

UIConverse comprises two main components:

- **ConversationalAgent:** Handles user prompts, delivering initial answers and suggestions for refinement. It maintains a conversation memory and splits outputs into initial answers and refinement suggestions.
- **UIAgent:** Takes responses from the ConversationalAgent along with instructions for UI creation. It outputs structured JSON for the UI without retaining conversation memory.

UML Class Diagram

![UML Class Diagram](https://github.com/David-Sat/ui-converse/blob/main/class_diagram.drawio.png)

### Future Directions

We plan to expand the capabilities of our system, including:

- **Enhancing the UIAgent:** Fine-tuning with diverse sets of custom-created UIs.
- **Autonomous Agent Development:** Utilizing the UI as a tool for gathering human inputs for autonomous decision-making.
- **Advanced UI Elements:** Introducing color pickers, date inputs, file uploaders, and more to enrich user interaction.
- **Data Analysis Enhancements:** Enabling users to upload datasets for analysis by an autonomous agent, further simplifying data interpretation and decision-making processes.

## Installation

- Install dependencies using `pip install -r requirements.txt`.
- Provide API keys for OpenAI and Gemini in streamlits `secrets.toml`.
- Launch the application with `streamlit run main.py`.
