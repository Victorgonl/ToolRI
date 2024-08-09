import functools
import tkinter.colorchooser

from ..styles import *
from .panel import Panel

if typing.TYPE_CHECKING:
    from ...controller import ToolRIController


class SettingsManager(Panel):

    def __init__(
        self, master: customtkinter.CTkFrame, toolri_controller: "ToolRIController"
    ) -> None:
        super().__init__(master, toolri_controller=toolri_controller)
        self.__settings_frame = self.__init_settings_frame()
        self.__options_frame = self.__init_options_frame()
        self.__box_options_buttons: dict[str, customtkinter.CTkRadioButton] = {}
        self.__visual_options_buttons: dict[str, customtkinter.CTkSwitch] = {}
        self.__labels_settings_buttons: dict[str, customtkinter.CTkSwitch] = {}
        self.__labels_frame = None

    def __init_settings_frame(self):
        settings_frame = ToolRIFrame(self._master)
        settings_frame.pack(padx=(5, 0))
        return settings_frame

    def __init_options_frame(self):
        frame = ToolRIFrame(master=self.__settings_frame)
        frame.pack(side="left", padx=(5, 0))
        return frame

    def set_box_options(self, box_options: list[str], initial_box_option: str):
        box_options_frame = ToolRIFrame(master=self.__options_frame)
        box_options_frame.pack(side="top", pady=(5, 0), padx=(0, 5))
        label = ToolRILabel(master=box_options_frame, text="Box Options")
        label.grid(pady=(0, 0))
        for i, option in enumerate(box_options):
            button = ToolRIRadioButton(
                master=box_options_frame,
                command=functools.partial(self.__select_box_option, option),
                variable=None,
                value=option,
                text=option,
            )
            button.grid(sticky="nw", pady=(0, 5))
            self.__box_options_buttons[option] = button
        self.__select_box_option(box_option=initial_box_option)

    def set_visual_options(
        self, visual_options: list, visual_options_values: list[bool]
    ):
        assert len(visual_options) == len(visual_options_values)
        visual_options_frame = ToolRIFrame(master=self.__options_frame)
        visual_options_frame.pack(side="bottom", pady=(5, 0), padx=(0, 5))
        label = ToolRILabel(master=visual_options_frame, text="Visual Options")
        label.grid(pady=(0, 0))
        for i, option in enumerate(visual_options):
            button = ToolRISwitch(
                master=visual_options_frame,
                command=functools.partial(
                    self._toolri_controller.toggle_option_active, option
                ),
                text=option,
            )
            button.grid(sticky="nw", pady=(5, 0), padx=(0, 5))
            self.__visual_options_buttons[option] = button
            if visual_options_values[i]:
                button.select()

    def set_labels_buttons(
        self,
        labels_names: list,
        labels_colors: list[str],
        labels_visibility: list[bool],
    ):
        assert len(labels_names) == len(labels_colors) == len(labels_visibility)
        if self.__labels_frame is not None:
            self.__labels_frame.destroy()
        self.__labels_frame = ToolRIFrame(master=self.__settings_frame)
        self.__labels_frame.pack(side="right", pady=(10, 0))
        label = ToolRILabel(master=self.__labels_frame, text="Labels Settings")
        label.grid(row=0)
        labels_tab = ToolRITabView(master=self.__labels_frame)
        labels_tab.grid(pady=(0, 0))
        last_tab_name = 0
        for i, label_name in enumerate(labels_names):
            if i % self._MAX_LABELS == 0:
                last_tab_name += 1
                labels_tab.add(str(last_tab_name))
            switch = ToolRISwitch(
                master=labels_tab.tab(name=str(last_tab_name)),
                command=functools.partial(
                    self._toolri_controller.toggle_label_visibility, label_name
                ),
                text_color=labels_colors[i],
                progress_color=labels_colors[i],
                text="",
            )
            switch.grid(row=i, column=0, sticky="nw", padx=(0, 0), pady=(5, 0))
            button = ToolRIButton(
                master=labels_tab.tab(name=str(last_tab_name)),
                command=functools.partial(self.__edit_label, label_name),
                text_color=labels_colors[i],
                text=(
                    label_name
                    if len(label_name) <= self._MAX_LABEL_NAME_LEN
                    else f"{label_name[:self._MAX_LABEL_NAME_LEN]}..."
                ),
            )
            button.grid(row=i, column=1, sticky="nw")
            self.__labels_settings_buttons[label_name] = switch
            if labels_visibility[i]:
                switch.select()
        create_label_button = ToolRIButton(
            master=self.__labels_frame, text="Create Label", command=self.__edit_label
        )
        create_label_button.grid()

    def __select_box_option(self, box_option):
        for bo in self.__box_options_buttons:
            if bo != box_option:
                self.__box_options_buttons[bo].deselect()
            else:
                self.__box_options_buttons[bo].select()
        self._toolri_controller.set_box_option(box_option=box_option)

    def __edit_label(self, label_name=None):

        edit_label_window = self._create_function_window(
            master=self._master, title="Edit Label"
        )
        edit_label_frame = ToolRIFrame(master=edit_label_window)
        edit_label_frame.pack(padx=15, pady=15)

        labels = self._toolri_controller.get_labels()
        if label_name is not None:
            label = self._toolri_controller.get_label(label_name=label_name)
            label_color = label.color
            links = label.links
        else:
            links = []
            label_color = "#FFFFFF"

        edit_frame = ToolRIFrame(master=edit_label_frame)
        edit_frame.pack()

        # edit name
        ToolRILabel(master=edit_frame, text="Name:").grid(
            row=0, column=0, sticky="nw", padx=(0, 5), pady=(10, 0)
        )
        label_name_variable = tkinter.StringVar(master=edit_frame, value=label_name)
        label_name_editor = ToolRIEntry(
            master=edit_frame,
            placeholder_text="Label Name",
            textvariable=label_name_variable,
        )
        label_name_editor.focus_force()
        label_name_editor.grid(row=0, column=1, sticky="nw", padx=(0, 5), pady=(10, 0))

        label_color_button = None

        def __choose_color():
            nonlocal label_color
            label_color = tkinter.colorchooser.askcolor(
                initialcolor=label_color, title="Label Color"
            )[1]
            if label_color is not None and label_color_button is not None:
                label_color = label_color.upper()
                label_color_button.configure(text=label_color, text_color=label_color)
                if self_button is not None:
                    self_button.configure(
                        text_color=label_color,
                        fg_color=label_color,
                        border_color=label_color,
                        hover_color=darken_hex_color(label_color),
                    )

        def __edit_label():
            nonlocal links
            if edit_label_window is not None:
                new_label_name = label_name_variable.get()
                self._toolri_controller.edit_label(
                    label_name, new_label_name, label_color, links
                )
                self._destroy_function_window()

        def __create_label():
            nonlocal links
            nonlocal self_link
            if edit_label_window is not None:
                new_label_name = label_name_variable.get()
                if self_link:
                    links.append(new_label_name)
                self._toolri_controller.create_label(new_label_name, label_color, links)
                self._destroy_function_window()

        def __delete_label():
            if edit_label_window is not None:
                self._toolri_controller.delete_label(label_name)
                self._destroy_function_window()

        def __toggle_link(link_label):
            nonlocal links
            if link_label in links:
                links.remove(link_label)
            else:
                links.append(link_label)

        def __toggle__self_link():
            nonlocal self_link
            self_link = not self_link

        __function = __edit_label if label_name is not None else __create_label

        # edit color
        ToolRILabel(master=edit_frame, text="Color:").grid(
            row=1, column=0, sticky="nw", pady=(10, 0)
        )
        label_color_button = ToolRIButton(
            master=edit_frame,
            text=label_color,
            command=__choose_color,
            text_color=label_color,
        )
        label_color_button.grid(row=1, column=1, sticky="nw", pady=(10, 0))

        # edit allowed links
        ToolRILabel(master=edit_frame, text="Links:").grid(
            row=2, column=0, sticky="nw", pady=(10, 0)
        )
        links_frame = ToolRITabView(master=edit_frame)
        links_frame.grid(row=2, column=1)
        self_button = None
        self_link = False
        last_tab_name = 0
        last_row = 0
        for i, label in enumerate(labels):
            if label_name is None and i == 0:
                last_tab_name += 1
                links_frame.add(str(last_tab_name))
                self_button = ToolRICheckBox(
                    master=links_frame.tab(name=str(last_tab_name)),
                    command=__toggle__self_link,
                    text_color=label_color,
                    checkmark_color=label_color,
                    text="Self",
                    onvalue=True,
                )
                self_button.grid(row=last_row, column=0, sticky="ew")
                last_row += 1
            if last_row % self._MAX_LABELS == 0:
                last_tab_name += 1
                links_frame.add(str(last_tab_name))
            button = ToolRICheckBox(
                master=links_frame.tab(name=str(last_tab_name)),
                command=functools.partial(__toggle_link, label.name),
                text_color=label.color,
                checkmark_color=label.color,
                text=(
                    label.name
                    if len(label.name) <= self._MAX_LABEL_NAME_LEN
                    else f"{label.name[:self._MAX_LABEL_NAME_LEN]}..."
                ),
                onvalue=True,
            )
            if label.name in links:
                button.select()
            button.grid(row=last_row, column=0, sticky="ew")
            last_row += 1

        # apply changes or delete label
        apply_and_cancel_frame = ToolRIFrame(master=edit_label_frame)
        apply_and_cancel_frame.pack(pady=(10, 0))
        ToolRIButton(
            master=apply_and_cancel_frame, text="Apply", command=__function
        ).pack(side="left")
        if label_name is not None:
            ToolRIButton(
                master=apply_and_cancel_frame, text="Delete", command=__delete_label
            ).pack(side="left")
