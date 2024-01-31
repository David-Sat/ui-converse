
from pydantic import BaseModel, Field, validator
from typing import List, Union, Tuple

class BaseUIElement(BaseModel):
    type: str = Field(description="Type of the UI element")
    label: str = Field(description="Label for the UI element")

class RadioButtons(BaseUIElement):
    options: List[str] = Field(description="Options for the radio buttons")

    @validator('options')
    def must_have_multiple_options(cls, v):
        if len(v) < 2:
            raise ValueError('RadioButtons must have 2 or more options')
        return v

class Slider(BaseUIElement):
    range: Tuple[int, int] = Field(description="Range for the slider")

class MultiSelect(BaseUIElement):
    options: List[str] = Field(description="Options for the multi-select")

class Checkbox(BaseUIElement):
    options: List[str] = Field(description="Options for the checkboxes")

class Output(BaseModel):
    title: str = Field(description="Title of the output")
    ui_elements: List[Union[RadioButtons, Slider, MultiSelect, Checkbox]] = Field(description="List of UI elements based on the suggestions after ␃. The text before ␃ is already displayed.")
