import tkinter

import customtkinter

from ..styles import *
from .panel import Panel

if typing.TYPE_CHECKING:
    from ...controller import ToolRIController

PADX = 2


class ToolPicker(Panel):

    def __init__(
        self, master: customtkinter.CTkFrame, toolri_controller: "ToolRIController"
    ) -> None:
        super().__init__(master, toolri_controller)
        self.__tools_buttons_frame: typing.Union[None, customtkinter.CTkFrame] = None
        self.labels_buttons = {}
        self.__tools_buttons = {}
        self.labels_buttons_frame = None
        self.__current_tool_name = None

    def set_tools(self, tools_names: list[str]):
        if tools_names:
            if self.__tools_buttons_frame is not None:
                self.__tools_buttons_frame.destroy()
            self.__tools_buttons_frame = ToolRIFrame(self._master)
            self.__tools_buttons_frame.pack(side="top", expand=True)
            tools_button = ToolRISegmentedButton(
                master=self.__tools_buttons_frame,
                texts=tools_names,
                command=self._toolri_controller.select_tool,
            )
            tools_button.set(
                tools_names[0], from_button_callback=True, from_variable_callback=True
            )
            tools_button.pack(fill="y", pady=7)
