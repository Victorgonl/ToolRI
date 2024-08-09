import customtkinter

from .color import *
from .text import *

LABEL_WIDTH = 25
LABEL_BG_COLOR = "transparent"
LABEL_FG_COLOR = None


def ToolRILabel(
    master,
    text,
    text_color=TEXT_COLOR,
    compound="center",
    width=LABEL_WIDTH,
    font=TEXT,
    fg_color=LABEL_FG_COLOR,
):
    return customtkinter.CTkLabel(
        master=master,
        text=text,
        width=width,
        text_color=text_color,
        fg_color=fg_color,
        bg_color=LABEL_BG_COLOR,
        font=font,
        compound=compound,
    )
