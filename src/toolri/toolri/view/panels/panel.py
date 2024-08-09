import typing

import customtkinter

from ..styles import ToolRIWindow

if typing.TYPE_CHECKING:
    from ...controller import ToolRIController


class Panel:

    _MAX_LABELS = 4
    _MAX_WORDS = 10
    _MAX_LINKS = 5
    _MAX_TEXT_SIZE = 25
    _MAX_LABEL_NAME_LEN = 10

    __function_window: typing.Union[None, customtkinter.CTkToplevel] = None

    def __init__(
        self, master: customtkinter.CTkFrame, toolri_controller: "ToolRIController"
    ) -> None:
        self._master = master
        self._toolri_controller = toolri_controller

    @classmethod
    def _create_function_window(cls, master, title):
        cls._destroy_function_window()
        cls.__function_window = ToolRIWindow(master=master, title=title)
        cls.__function_window.protocol("WM_DELETE_WINDOW", cls._destroy_function_window)
        return cls.__function_window

    @classmethod
    def _destroy_function_window(cls):
        if cls.__function_window is not None:
            cls.__function_window.destroy()
            cls.__function_window = None

    def _bind_key(self, key, function):
        self._master.master.bind(key, function)

    def _set_timer_function(self, time, function):
        self._master.master.after(time, function)
