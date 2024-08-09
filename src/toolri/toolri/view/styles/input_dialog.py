import customtkinter

from .color import *
from .text import *


def ToolRIInputDialog(text, title):
    input_dialog = customtkinter.CTkInputDialog(text=text, title=title, font=TEXT)
    a = customtkinter.CTkToplevel
    return input_dialog
