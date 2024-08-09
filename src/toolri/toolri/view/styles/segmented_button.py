import customtkinter

from .style_functions import darken_hex_color
from .text import *
from .color import *

BUTTON_BG_COLOR = "transparent"
SEGMENTED_BUTTON_CORNER_RADIUS = 10
BUTTON_FG_COLOR = FG_COLOR
BUTTON_TEXT_COLOR = TEXT_COLOR
BUTTON_HOVER_COLOR = HOVER_COLOR
BUTTON_WIDTH = 50
SEGMENTED_BUTTON_BORDER_WIDHT = 1


def ToolRISegmentedButton(
    master, texts, command, width=BUTTON_WIDTH, text_color=BUTTON_TEXT_COLOR
):
    button = customtkinter.CTkSegmentedButton(
        master,
        values=texts,
        command=command,
        width=width,
        border_width=SEGMENTED_BUTTON_BORDER_WIDHT,
        font=TEXT,
        bg_color=BUTTON_BG_COLOR,
        corner_radius=SEGMENTED_BUTTON_CORNER_RADIUS,
        fg_color=BUTTON_FG_COLOR,
        text_color=text_color,
        unselected_color=BUTTON_FG_COLOR,
        unselected_hover_color=BUTTON_HOVER_COLOR,
        selected_color=BUTTON_HOVER_COLOR,
        selected_hover_color=BUTTON_HOVER_COLOR,
    )
    return button
