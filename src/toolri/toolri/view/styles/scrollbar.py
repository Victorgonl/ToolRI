import customtkinter

from .color import *


def ToolRIScrollbar(master, orientation, command=None):
    scrollbar = customtkinter.CTkScrollbar(
        master=master,
        orientation=orientation,
        command=command,
        fg_color=FG_COLOR,
        bg_color=BG_COLOR,
    )
    return scrollbar
