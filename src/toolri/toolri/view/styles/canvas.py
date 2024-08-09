import customtkinter

from .color import *

CANVAS_BG_COLOR = BG_COLOR
CANVAS_HIGHLIGHTTHICKNESS = 0


def ToolRICanvas(master, width=200, height=200, bg=CANVAS_BG_COLOR):
    canvas = customtkinter.CTkCanvas(
        master,
        width=width,
        height=height,
        bg=bg,
        highlightthickness=CANVAS_HIGHLIGHTTHICKNESS,
    )
    return canvas
