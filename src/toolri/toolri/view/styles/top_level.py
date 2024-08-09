import customtkinter

from .color import *


def ToolRITopLevel(master, title: str, width=500, height=500):
    top_level = customtkinter.CTkToplevel(master=master,
                                          width=width,
                                          height=height,
                                          fg_color=FG_COLOR)
    top_level.title(title)
    return top_level
