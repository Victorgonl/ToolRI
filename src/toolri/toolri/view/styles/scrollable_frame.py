import customtkinter

from .frame import *
from .text import TEXT

FRAME_FG_COLOR = FG_COLOR
FRAME_BG_COLOR = BG_COLOR
FRAME_BORDER_COLOR = FRAME_BG_COLOR


def ToolRIScrollableFrame(master,
                          width=200,
                          height=200,
                          border_width=None,
                          corner_radius=None,
                          fg_color=FRAME_FG_COLOR,
                          label_text="",
                          scrollbar_button_color=FG_COLOR):
    frame = customtkinter.CTkScrollableFrame(
        master,
        width=width,
        height=height,
        bg_color=FRAME_BG_COLOR,
        fg_color=fg_color,
        border_width=border_width,
        border_color=FRAME_BORDER_COLOR,
        corner_radius=corner_radius,
        label_text=label_text,
        label_text_color=TEXT_COLOR,
        label_font=TEXT,
        label_fg_color=FRAME_FG_COLOR,
        scrollbar_button_color=scrollbar_button_color)
    return frame
