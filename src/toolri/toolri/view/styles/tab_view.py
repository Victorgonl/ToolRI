import customtkinter

from .color import *
from .segmented_button import *

TAB_VIEW_BG_COLOR = BG_COLOR
TAB_VIEW_FG_COLOR = FG_COLOR


def ToolRITabView(
    master,
    width=1,
    height=1,
    border_width=None,
    fg_color=TAB_VIEW_FG_COLOR,
    font=TEXT,
):
    tab_view = customtkinter.CTkTabview(
        master=master,
        width=width,
        height=height,
        corner_radius=SEGMENTED_BUTTON_CORNER_RADIUS,
        bg_color=TAB_VIEW_BG_COLOR,
        fg_color=fg_color,
        border_width=border_width,
        border_color=TAB_VIEW_FG_COLOR,
        segmented_button_fg_color=TAB_VIEW_FG_COLOR,
        segmented_button_selected_color=BUTTON_HOVER_COLOR,
        segmented_button_selected_hover_color=BUTTON_HOVER_COLOR,
        segmented_button_unselected_color=BUTTON_FG_COLOR,
        segmented_button_unselected_hover_color=BUTTON_HOVER_COLOR,
    )
    tab_view._segmented_button.configure(font=font)
    return tab_view
