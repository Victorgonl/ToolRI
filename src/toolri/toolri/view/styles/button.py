import customtkinter

from .color import *
from .style_functions import darken_hex_color
from .text import *

BUTTON_BG_COLOR = "transparent"
BUTTON_CORNER_RADIUS = None
BUTTON_FG_COLOR = FG_COLOR
BUTTON_TEXT_COLOR = TEXT_COLOR
BUTTON_HOVER_COLOR = HOVER_COLOR
BUTTON_WIDTH = 50


def ToolRIButton(
    master,
    text,
    command,
    anchor="center",
    width=BUTTON_WIDTH,
    text_color=BUTTON_TEXT_COLOR,
    fg_color=BUTTON_FG_COLOR,
    corner_radius=BUTTON_CORNER_RADIUS,
):
    button = customtkinter.CTkButton(
        master,
        text=text,
        command=command,
        width=width,
        font=TEXT,
        bg_color=BUTTON_BG_COLOR,
        fg_color=fg_color,
        hover_color=BUTTON_HOVER_COLOR,
        text_color=text_color,
        text_color_disabled=darken_hex_color(text_color),
        corner_radius=corner_radius,
        anchor=anchor,
    )
    return button
