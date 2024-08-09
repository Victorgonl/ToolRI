import enum
import functools
import tkinter
import typing

import customtkinter

from ..styles import *
from .panel import Panel

if typing.TYPE_CHECKING:
    from ...controller import ToolRIController


NULL_NAME = "---"


class DataEditorOptions(enum.Enum):
    DATA = "Data"
    JSON = "JSON"


class DataManager(Panel):

    __NULL_FILE_NAME = "---"

    def __init__(
        self, master: customtkinter.CTkFrame, toolri_controller: "ToolRIController"
    ) -> None:
        super().__init__(master, toolri_controller)

        if self._toolri_controller.is_binary_instance:
            self.__data_filename, self.__image_filename, self.__save_data_button = (
                self.__init_load_and_save_buttons()
            )
        self.__data_editor_frame = self.__init_tabview()
        self.__json_data_frame = self.__init_json_data_frame(self.__data_editor_frame)
        self.__data_buttons_frame = self.__init_data_editor(self.__data_editor_frame)
        self.__data_buttons: dict[int, customtkinter.CTkButton] = {}

        self.__init_clear_buttons()

    def set_data_file_name(self, data_file_name: str):
        data_file_name = data_file_name if data_file_name else NULL_NAME
        self.__data_filename.configure(text=data_file_name)  # type: ignore

    def set_image_file_name(self, image_file_name: str):
        image_file_name = image_file_name if image_file_name else NULL_NAME
        self.__image_filename.configure(text=image_file_name)  # type: ignore

    def set_json_data(self, json_data: str):
        self.__json_data_frame.delete("1.0", "end")
        self.__json_data_frame.insert(
            index="end",
            text=json_data,
        )

    def get_json_data(self):
        return self.__json_data_frame.get("1.0", "end-1c")

    def __init_clear_buttons(self):
        clear_labels_button = ToolRIButton(
            self._master,
            text="Clear Labels",
            command=functools.partial(self._toolri_controller.clear_data, "labels"),
        )
        clear_links_button = ToolRIButton(
            self._master,
            text="Clear Links",
            command=functools.partial(self._toolri_controller.clear_data, "links"),
        )
        clear_button = ToolRIButton(
            self._master,
            text="Clear Data",
            command=functools.partial(self._toolri_controller.clear_data, "data"),
        )
        clear_button.pack(side="bottom", fill="x", expand=False)
        clear_labels_button.pack(side="bottom", fill="x", expand=False)
        clear_links_button.pack(side="bottom", fill="x", expand=False)

    def __init_json_data_frame(self, tabview):

        frame = ToolRIFrame(tabview.tab(DataEditorOptions.JSON.value))
        text = ToolRITextBox(frame, corner_radius=25)
        text.insert(
            index="end",
            text="[]",
        )
        apply_button = ToolRIButton(
            frame, text="Apply", command=self._toolri_controller.apply_json_data
        )
        text.pack(side="top", expand=True, fill="both")
        apply_button.pack(side="bottom", expand=False, pady=5)
        frame.pack(expand=True, fill="both")
        return text

    def __init_data_editor(self, tabview):
        data_editor_frame = ToolRIScrollableFrame(
            tabview.tab(DataEditorOptions.DATA.value),
            corner_radius=25,
            fg_color=TEXT_FG_COLOR,
            scrollbar_button_color=TEXT_FG_COLOR,
        )
        data_editor_frame.pack(expand=True, fill="both")
        return data_editor_frame

    def __init_tabview(self):

        tabview = ToolRITabView(self._master, width=250, border_width=10)
        tabview.pack(expand=True, fill="both")
        tabview.add(DataEditorOptions.DATA.value)
        tabview.add(DataEditorOptions.JSON.value)

        return tabview

    def __sort_buttons(self):
        entity_ids = list(self.__data_buttons.keys())
        sorted_entity_ids = sorted(entity_ids)
        for index, entity_id in enumerate(sorted_entity_ids):
            entity_button = self.__data_buttons[entity_id]
            entity_button.grid(row=index, column=0, sticky="w")

    def add_entity_button(self, entity_id, entity_title, color):
        if entity_id in self.__data_buttons:
            self.update_entity_button(entity_id, entity_title, color)
        entity_button = ToolRIButton(
            self.__data_buttons_frame,
            text="",
            command=functools.partial(self.__edit_entity, entity_id),
            fg_color=TEXT_FG_COLOR,
        )
        entity_button.grid(sticky="w")
        self.__data_buttons[entity_id] = entity_button
        self.update_entity_button(entity_id, entity_title, color)

    def update_entity_button(self, entity_id, entity_title, color):
        if color == "#000000":
            color = "#FFFFFF"
        entity_button = self.__data_buttons[entity_id]
        entity_button.configure(
            text=f"{entity_id}: {entity_title}", text_color=color, require_redraw=True
        )
        self.__data_buttons[entity_id] = entity_button
        self.__sort_buttons()

    def update_save_data_button(self, is_data_changed: bool):
        if is_data_changed:
            self.__save_data_button.configure(text="*Save Data")
        else:
            self.__save_data_button.configure(text="Save Data")

    def delete_entity_button(self, entity_id):
        self.__data_buttons[entity_id].destroy()
        del self.__data_buttons[entity_id]

    def get_entity_buttons_ids(self):
        return list(self.__data_buttons.keys())

    def open_file(self, initialdir, filetypes):
        path = customtkinter.filedialog.askopenfilename(
            initialdir=initialdir,
            filetypes=filetypes,
        )
        return path

    def save_file(self, initialfile, defaultextension, initialdir, filetypes):
        path = customtkinter.filedialog.asksaveasfilename(
            initialfile=initialfile,
            defaultextension=defaultextension,
            initialdir=initialdir,
            filetypes=filetypes,
        )
        return path

    def __init_load_and_save_buttons(self):

        open_image_button = ToolRIButton(
            self._master, text="Load Image", command=self._toolri_controller.load_image
        )
        open_image_button.pack(side="top", fill="x", expand=False)
        image_filename = ToolRILabel(
            self._master,
            text=self.__NULL_FILE_NAME,
        )
        image_filename.pack()

        open_data_button = ToolRIButton(
            self._master, text="Load Data", command=self._toolri_controller.load_data
        )
        open_data_button.pack(side="top", fill="x", expand=False)
        data_filename = ToolRILabel(
            self._master,
            text=self.__NULL_FILE_NAME,
        )
        data_filename.pack()

        save_data_button = ToolRIButton(
            self._master, text="Save Data", command=self._toolri_controller.save_data
        )
        save_data_button.pack(side="top", fill="x", expand=False)

        return data_filename, image_filename, save_data_button

    def __edit_entity(self, entity_id):

        def __edit_entity():
            words = [word_editor.get() for word_editor in words_editors]
            label = label_variable.get()
            self._toolri_controller.edit_entity(
                entity_id=entity.id, words=words, label=label
            )
            self._destroy_function_window()

        """ def __toggle_link(entity_id):
            new_links[entity_id] = not new_links[entity_id]
            for button in links_buttons:
                label = button.get()
                if not self._toolri_controller.settings.is_link_allowed(
                    parent_entity_label=entity_id.label, child_entity_label=label
                ):
                    button.configure(state=tkinter.DISABLED) """

        def __delete_entity():
            self._toolri_controller.delete_entity(entity_id=entity.id)
            self._destroy_function_window()

        # entity and labels
        entities = self._toolri_controller.get_entities()
        entity = self._toolri_controller.get_entity(entity_id)
        labels = self._toolri_controller.get_labels()

        # editor window
        edit_entity_window = self._create_function_window(
            master=self._master, title=f"Edit Entity: {entity_id}"
        )
        edit_label_frame = ToolRIFrame(master=edit_entity_window)
        edit_label_frame.pack(padx=15, pady=15)

        # edit frame
        edit_frame = ToolRIFrame(master=edit_label_frame)
        edit_frame.pack()

        # edit words
        words_frame = ToolRITabView(master=edit_frame)
        words_frame.grid()
        ToolRILabel(master=edit_frame, text="Words:").grid(
            row=0, column=0, sticky="nw", padx=(0, 5), pady=(10, 0)
        )
        words_variables = []
        words_editors: list[customtkinter.CTkEntry] = []
        last_tab_name = 0
        for i, word in enumerate(entity.words):
            if i % self._MAX_WORDS == 0:
                last_tab_name += 1
                words_frame.add(str(last_tab_name))
            word_variable = tkinter.StringVar(master=edit_frame, value=word)
            word_editor = ToolRIEntry(
                master=words_frame.tab(str(last_tab_name)),
                placeholder_text="Entity word",
                textvariable=word_variable,
            )
            word_editor.focus_force()
            word_editor.grid(row=i, column=1, sticky="nw", padx=(0, 5), pady=(10, 0))
            words_variables.append(word_variable)
            words_editors.append(word_editor)
        words_editors[0].focus_force()

        def __check_if_label_is_allowed(label_name):
            for link in entity.links:
                if entity.id == link[0]:
                    if not self._toolri_controller.settings.is_link_allowed(
                        label_name, self._toolri_controller.get_entity(link[1]).label
                    ):
                        return False
                elif entity.id == link[1]:
                    if not self._toolri_controller.settings.is_link_allowed(
                        self._toolri_controller.get_entity(link[0]).label, label_name
                    ):
                        return False
            return True

        # edit label
        label_variable = tkinter.StringVar(master=edit_frame, value=entity.label)
        labels_frame = ToolRITabView(master=edit_frame)
        labels_frame.grid()
        ToolRILabel(master=edit_frame, text="Label:").grid(
            row=1,
            sticky="nw",
            padx=(0, 5),
            pady=(10, 0),
        )
        last_label_frame = None
        last_row = 0
        ll = [
            label
            for label in labels
            if __check_if_label_is_allowed(label_name=label.name)
        ]
        for i, label in enumerate(ll):
            if i % self._MAX_LABELS == 0:
                last_row += 1
                labels_frame.add(str(last_row))
            if i % self._MAX_LABELS == 0:
                last_label_frame = ToolRIFrame(master=labels_frame.tab(str(last_row)))
                last_label_frame.grid()
            label_button = ToolRIRadioButton(
                master=last_label_frame,
                command=None,
                color=label.color,
                text=(
                    label.name
                    if len(label.name) <= self._MAX_LABEL_NAME_LEN
                    else f"{label.name[:self._MAX_LABEL_NAME_LEN]}..."
                ),
                value=label.name,
                variable=label_variable,
            )
            if label.name == entity.label:
                label_button.select()
            label_button.grid(row=i, column=last_row - 1, sticky="ew", pady=(0, 5))

        # edit links
        """ new_links = {e.id: False for e in entities}
        links_buttons: list[customtkinter.CTkCheckBox] = []
        links_frame = ToolRITabView(master=edit_frame)
        links_frame.grid(padx=(25, 0))
        ToolRILabel(master=edit_frame, text="Links:").grid(
            row=2,
            sticky="nw",
            padx=(0, 5),
            pady=(10, 0),
        )
        last_row = 0
        for i, e in enumerate(entities):
            if i % self._MAX_LINKS == 0:
                last_row += 1
                links_frame.add(str(last_row))
            color = self._toolri_controller.get_label_color(e.label)
            link_button = ToolRICheckBox(
                master=links_frame.tab(str(last_row)),
                command=functools.partial(__toggle_link, e.id),
                checkmark_color=color,
                text=f"{e.id}: {e.text[:self._MAX_TEXT_SIZE]}",
                text_color=color,
                onvalue=e.id,
            )
            if any([entity.id == link[0] for link in e.links]):
                new_links[e.id] = True
                link_button.select()
            link_button.grid(row=i, column=0, sticky="ew")
            links_buttons.append(link_button) """

        # apply changes or delete label
        apply_and_cancel_frame = ToolRIFrame(master=edit_label_frame)
        apply_and_cancel_frame.pack(pady=(10, 0))
        ToolRIButton(
            master=apply_and_cancel_frame, text="Apply", command=__edit_entity
        ).pack(side="left")
        ToolRIButton(
            master=apply_and_cancel_frame, text="Delete", command=__delete_entity
        ).pack(side="left")
