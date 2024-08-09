import functools

import customtkinter

from ..styles import *
from .panel import Panel

if typing.TYPE_CHECKING:
    from ...controller import ToolRIController

PADX = 2


class LabelPicker(Panel):

    def __init__(
        self, master: customtkinter.CTkFrame, toolri_controller: "ToolRIController"
    ) -> None:
        super().__init__(master, toolri_controller)
        self.__labels_buttons: dict[str, customtkinter.CTkRadioButton] = {}
        self.__labels_buttons_frame: typing.Union[None, customtkinter.CTkFrame] = None

    def activate_labels_panel(
        self, labels_names: list[str], labels_colors, active_label=None
    ):
        assert len(labels_names) == len(labels_colors)
        self.deactivate_labels_panel()
        if labels_names:
            self.__labels_buttons_frame = ToolRIFrame(self._master)
            self.__labels_buttons_frame.pack(side="top", expand=True)
            for i, (label_name, label_color) in enumerate(
                zip(labels_names, labels_colors)
            ):
                if i % (self._MAX_LABELS) == 0:
                    labels_frame = ToolRIFrame(master=self.__labels_buttons_frame)
                    labels_frame.pack()
                label_button = ToolRIRadioButton(
                    master=labels_frame,
                    text=(
                        label_name
                        if len(label_name) <= self._MAX_LABEL_NAME_LEN
                        else f"{label_name[:self._MAX_LABEL_NAME_LEN]}..."
                    ),
                    color=label_color,
                    command=functools.partial(self.__select_label_button, label_name),
                    value=label_name,
                )
                label_button.pack(side="left", pady=(0, 5), padx=10)
                self.__labels_buttons[label_name] = label_button
            if active_label is None:
                active_label = labels_names[0]
            self.__select_label_button(label_name=active_label)

    def deactivate_labels_panel(self):
        if self.__labels_buttons_frame is not None:
            self.__labels_buttons_frame.destroy()
            self.__labels_buttons = {}

    def __select_label_button(self, label_name):
        for ln in self.__labels_buttons:
            if ln != label_name:
                self.__labels_buttons[ln].deselect()
            else:
                self.__labels_buttons[ln].select()
        self._toolri_controller.select_active_label(label_name=label_name)
