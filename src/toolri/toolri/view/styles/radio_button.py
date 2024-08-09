import customtkinter

from .button import *
from .color import *
from .style_functions import darken_hex_color
from .text import *

BUTTON_BG_COLOR = "transparent"
RADIO_BUTTON_FG_COLOR = WHITE
RADIO_BUTTON_WIDTH = 15
RADIO_BUTTON_BORDER_CHECKED = 5
RADIO_BUTTON_BORDER_UNCHECKED = 3


def ToolRIRadioButton(
    master, command, value, text, variable=None, color=RADIO_BUTTON_FG_COLOR
):
    radio_button = customtkinter.CTkRadioButton(
        master,
        width=1,
        height=1,
        text=text,
        variable=variable,
        command=command,
        value=value,
        font=TEXT,
        fg_color=color,
        hover_color=darken_hex_color(color),
        border_color=color,
        text_color=color,
        text_color_disabled=darken_hex_color(color),
        radiobutton_width=RADIO_BUTTON_WIDTH,
        radiobutton_height=RADIO_BUTTON_WIDTH,
        border_width_checked=RADIO_BUTTON_BORDER_CHECKED,
        border_width_unchecked=RADIO_BUTTON_BORDER_UNCHECKED,
    )
    return radio_button
