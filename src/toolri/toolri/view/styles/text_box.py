import customtkinter

from .color import *
from .text import *

TEXT_BOX_WIDTH = 200
TEXT_BOX_FONT = TEXT_BOX_SMALL
TEXT_BOX_FG_COLOR = TEXT_FG_COLOR
TEXT_BOX_TEXT_COLOR = TEXT_COLOR
TEXT_BOX_BORDER_COLOR = BG_COLOR


def ToolRITextBox(master, width=TEXT_BOX_WIDTH, corner_radius=None, border_width=None):
    text_box = customtkinter.CTkTextbox(
        master=master,
        width=width,
        font=TEXT_BOX_FONT,
        fg_color=TEXT_BOX_FG_COLOR,
        text_color=TEXT_BOX_TEXT_COLOR,
        corner_radius=corner_radius,
        border_width=border_width,
        border_color=TEXT_BOX_BORDER_COLOR,
    )

    def select_text(event):
        text_box.tag_add("sel", 1.0, "end")
        text_box.mark_set("insert", 1.0)
        text_box.see("insert")
        return "break"

    text_box.bind("<Control-a>", select_text)
    return text_box
