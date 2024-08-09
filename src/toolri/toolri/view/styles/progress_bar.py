import customtkinter

from .color import *


def ToolRIProgressBar(master, width=None):
    progress_bar = customtkinter.CTkProgressBar(
        master=master, width=300, progress_color=TEXT_COLOR, fg_color=None
    )
    return progress_bar
