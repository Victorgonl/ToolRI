import customtkinter

from .style_functions import darken_hex_color
from .color import *
from .text import *

ENTRY_WIDTH = 170
ENTRY_FG_COLOR = TEXT_FG_COLOR
ENTRY_BG_COLOR = TEXT_FG_COLOR
ENTRY_TEXT_COLOR = TEXT_COLOR
ENTRY_TEXT_FONT = TEXT_BOX
ENTRY_PLACEHOLDER = "..."


def ToolRIEntry(
    master,
    width=ENTRY_WIDTH,
    placeholder_text=ENTRY_PLACEHOLDER,
    justify=None,
    textvariable=None,
):
    entry = customtkinter.CTkEntry(
        master=master,
        width=width,
        corner_radius=5,
        bg_color="transparent",
        fg_color=ENTRY_FG_COLOR,
        text_color=ENTRY_TEXT_COLOR,
        font=ENTRY_TEXT_FONT,
        placeholder_text=placeholder_text,
        placeholder_text_color=darken_hex_color(ENTRY_TEXT_COLOR, factor=0.5),
        justify=justify,
        textvariable=textvariable,
    )

    def select_text(event):
        # select text
        event.widget.select_range(0, "end")
        # move cursor to the end
        event.widget.icursor("end")
        # stop propagation
        return "break"

    def unselect_text(event):
        # deselect text
        event.widget.selection_clear()
        return "break"

    entry.bind("<Control-a>", select_text)
    entry.bind("<FocusIn>", select_text)
    entry.bind("<FocusOut>", unselect_text)

    return entry
