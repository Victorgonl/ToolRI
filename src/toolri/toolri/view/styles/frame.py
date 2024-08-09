import customtkinter

from .color import *

FRAME_FG_COLOR = FG_COLOR
FRAME_BG_COLOR = BG_COLOR
FRAME_BORDER_COLOR = FRAME_BG_COLOR


def ToolRIFrame(
    master,
    width=1,
    height=1,
    border_width=None,
    corner_radius=None,
    fg_color=FRAME_FG_COLOR,
    bg_color=FRAME_BG_COLOR,
):
    frame = customtkinter.CTkFrame(
        master,
        width=width,
        height=height,
        bg_color=bg_color,
        fg_color=fg_color,
        border_width=border_width,
        border_color=FRAME_BORDER_COLOR,
        corner_radius=corner_radius,
    )
    return frame
