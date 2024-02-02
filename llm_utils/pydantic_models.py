"""pydantic models for the UI elements and output structure."""
from typing import List, Union, Tuple
from pydantic import BaseModel, Field, validator


class BaseUIElement(BaseModel):
    """Defines a base model for UI elements with a type and label."""
    type: str = Field(description="Type of the UI element")
    label: str = Field(description="Label for the UI element")


class RadioButtons(BaseUIElement):
    """Represents radio buttons with multiple options."""
    options: List[str] = Field(description="Options for the radio buttons")

    @validator('options')
    @classmethod
    def must_have_multiple_options(cls, v):
        """Ensures radio buttons have 2 or more options."""
        if len(v) < 2:
            raise ValueError('RadioButtons must have 2 or more options')
        return v


class Slider(BaseUIElement):
    """Defines a slider with a specified range."""
    range: Tuple[int, int] = Field(description="Range for the slider")


class MultiSelect(BaseUIElement):
    """Represents a multi-select element with multiple options."""
    options: List[str] = Field(description="Options for the multi-select")


class Checkbox(BaseUIElement):
    """Defines checkboxes with multiple options."""
    options: List[str] = Field(description="Options for the checkboxes")


class Output(BaseModel):
    """Models the output structure with a title and various UI elements."""
    title: str = Field(description="Title of the output")
    ui_elements: List[Union[RadioButtons, Slider, MultiSelect, Checkbox]] = Field(
        description="List of UI elements based on the suggestions after ␃. The text before ␃ is already displayed.")
