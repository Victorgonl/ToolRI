import platform

import CTkMessagebox
import customtkinter

from ...version import NAME, URL, VERSION
from .panels import (
    DataManager,
    ImageCanvas,
    LabelPicker,
    SettingsManager,
    ToolPicker,
    WordsExtractor,
)
from .styles import *

if typing.TYPE_CHECKING:
    from ..controller import ToolRIController

MAIN_WINDOW_WIDTH = 1000


class ToolRIView:
    def __init__(self, toolri_controller) -> None:
        self.__window = self.__init_window()
        self.__toolri_controller = toolri_controller
        self.__frames = {}
        self.__init_panels()

    def __init_window(self):
        window = customtkinter.CTk()
        window.configure(bg=TEXT_FG_COLOR)
        window.title(f"{NAME} {VERSION}")
        window.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_WIDTH}")
        if platform.system() == "Windows":
            window.attributes("-alpha", True)
        else:
            window.attributes("-zoomed", True)
        window.update()
        return window

    def __create_frame(
        self,
        Panel,
        side: typing.Literal["right", "left", "top", "bottom"],
        expand: bool,
    ):
        if side not in self.__frames:
            frame = ToolRIFrame(self.__window)
            self.__frames[side] = frame
        else:
            frame = self.__frames[side]
        frame.pack(side=side, expand=expand, fill="both")
        panel = Panel(frame, self.__toolri_controller)
        return panel

    def __init_panels(self):

        self.__data_manager = self.__create_frame(
            DataManager, side="left", expand=False
        )
        self.__settings_manager = self.__create_frame(
            SettingsManager, side="right", expand=False
        )
        self.__words_extractor = self.__create_frame(
            WordsExtractor, side="right", expand=False
        )
        self.__image_canvas = self.__create_frame(
            ImageCanvas, side="bottom", expand=True
        )
        self.__tool_picker = self.__create_frame(ToolPicker, side="top", expand=False)
        self.__label_picker = self.__create_frame(LabelPicker, side="top", expand=False)

    @property
    def toolri_controller(self):
        return self.__toolri_controller

    @property
    def data_manager(self):
        return self.__data_manager

    @property
    def tool_picker(self):
        return self.__tool_picker

    @property
    def label_picker(self):
        return self.__label_picker

    @property
    def image_canvas(self):
        return self.__image_canvas

    @property
    def words_extractor(self):
        return self.__words_extractor

    @property
    def settings_manager(self):
        return self.__settings_manager

    def run(self):

        def on_close() -> None:
            msg = CTkMessagebox.CTkMessagebox(
                title="ToolRI",
                message="Close ToolRI without saving?",
                icon="question",
                option_1="No",
                option_2="Yes",
                fg_color=FG_COLOR,
            )
            response = msg.get()

            if response == "Yes":
                self.__window.destroy()

        # self.__window.protocol("WM_DELETE_WINDOW", on_close)
        self.__window.protocol("", on_close)
        self.__window.mainloop()
