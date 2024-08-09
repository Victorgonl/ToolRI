import customtkinter

from .color import *
from .style_functions import darken_hex_color
from .text import *

SWITCH_WIDTH = 40
SWITCH_HEIGHT = 15
SWITCH_FONT = TEXT
SWITCH_BUTTON_COLOR = TEXT_COLOR


def ToolRISwitch(
    master,
    command,
    text,
    width=1,
    height=1,
    text_color=SWITCH_BUTTON_COLOR,
    progress_color=SWITCH_BUTTON_COLOR,
    switch_width=SWITCH_WIDTH,
    switch_height=SWITCH_HEIGHT,
):
    switch = customtkinter.CTkSwitch(
        master=master,
        width=width,
        height=height,
        command=command,
        font=SWITCH_FONT,
        switch_width=switch_width,
        switch_height=switch_height,
        text=text,
        fg_color=FG_COLOR,
        button_color=SWITCH_BUTTON_COLOR,
        button_hover_color=darken_hex_color(SWITCH_BUTTON_COLOR),
        text_color=text_color,
        progress_color=progress_color,
    )
    return switch
