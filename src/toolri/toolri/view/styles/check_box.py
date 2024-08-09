import customtkinter

from .color import *
from .style_functions import darken_hex_color
from .text import *


def ToolRICheckBox(
    master,
    text,
    text_color,
    checkmark_color,
    onvalue,
    command=None,
    corner_radius=5,
    checkbox_width=20,
    checkbox_height=20,
    font=TEXT,
    variable=None,
):
    return customtkinter.CTkCheckBox(
        master=master,
        text=text,
        checkbox_width=checkbox_width,
        checkbox_height=checkbox_height,
        onvalue=onvalue,
        offvalue="",
        command=command,
        corner_radius=corner_radius,
        text_color=text_color,
        fg_color=checkmark_color,
        bg_color="transparent",
        font=font,
        hover_color=darken_hex_color(checkmark_color),
        border_color=checkmark_color,
        checkmark_color=FG_COLOR,
        variable=variable,
    )
