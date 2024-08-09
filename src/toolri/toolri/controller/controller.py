import os
import typing

import PIL.Image

from toolri.toolri.model.geometry_functions.geometry_functions import (
    box_mid_left_point,
    box_mid_point,
    box_mid_right_point,
)

from ..model import ToolRIData
from ..view import ToolRIView
from ..view.panels.image_canvas import DrawWidth
from .image_manager import ImageManager
from .settings import (
    BoxOptions,
    ToolRIInstance,
    ToolRILabel,
    ToolRISettings,
    VisualOptions,
)
from .tools import OCR, JoinSplit, Labeling, Linking, Manual, Tool

DATA_FILE_EXTENSIONS = ["json"]
IMAGE_FILE_EXTENSIONS = ["png", "jpg"]
OPEN_DATA_EXTENSIONS = [
    f"*.{image_extension}" for image_extension in DATA_FILE_EXTENSIONS
]
OPEN_IMAGE_EXTENSIONS = [
    f"*.{image_extension}" for image_extension in IMAGE_FILE_EXTENSIONS
]


class ToolRIController:

    DRAW_LINE_WIDTH = 3

    def __init__(
        self,
        image,
        data,
        toolri_instance: ToolRIInstance,
        labels: typing.Union[None, list[ToolRILabel]],
    ) -> None:

        # TODO: create a class for hold this
        self.__data_path = ""
        self.__data_file_name = ""
        self.__data_folder = ""
        self.__data_sample = ""
        self.__image_file_name = ""
        self.__image_path = ""
        self.__image_folder = ""
        self.__image_sample = ""

        self.__checkpoint_json_data = ""

        # TODO: this __init__ function is provisory and must be fixed
        self.__toolri_data = ToolRIData(entities_dict_list=data)
        self.__image_manager: ImageManager = ImageManager(image)
        self.__toolri_settings: ToolRISettings = ToolRISettings(
            toolri_instance=toolri_instance, labels=labels
        )
        self.__active_tool: typing.Union[None, Tool] = None
        self.__tools: dict[str, typing.Type[Tool]] = self.__init_tools()
        self.__toolri_view = ToolRIView(toolri_controller=self)
        self.__toolri_view.tool_picker.set_tools(tools_names=list(self.__tools.keys()))
        self.__toolri_view.settings_manager.set_box_options(
            box_options=[option.value for option in BoxOptions],
            initial_box_option=self.__toolri_settings.box_option,
        )
        self.__toolri_view.settings_manager.set_visual_options(
            visual_options=[option.value for option in VisualOptions],
            visual_options_values=[
                self.__toolri_settings.is_visual_option_active(option)
                for option in VisualOptions
            ],
        )

        self.__update_view(data_changed=True, image_changed=True, labels_changed=True)

    def __init_tools(self):
        tools = {}

        def __add_tool(Tool):
            tool_name = Tool.name
            tools[tool_name] = Tool

        __add_tool(OCR)
        __add_tool(Manual)
        __add_tool(JoinSplit)
        __add_tool(Linking)
        __add_tool(Labeling)

        return tools

    @property
    def is_binary_instance(self):
        return self.__toolri_settings.instance == ToolRIInstance.BINARY

    @property
    def settings(self):
        return self.__toolri_settings

    def select_tool(self, tool_name):
        self.__active_tool = self.__tools[tool_name](
            toolri_view=self.__toolri_view,
            toolri_settings=self.__toolri_settings,
            toolri_image=self.__image_manager,
            toolri_data=self.__toolri_data,
        )
        self.__update_label_picker_panel()

    def receive_mouse_function(
        self,
        geometry_or_point: typing.Union[tuple[int, int, int, int], tuple[int, int]],
        mouse_button: typing.Literal["right", "left"],
    ):
        if self.__active_tool is not None:
            if mouse_button == "left":
                data_changed = self.__active_tool._primary_function(geometry_or_point)  # type: ignore
            if mouse_button == "right":
                data_changed = self.__active_tool._secondary_function(geometry_or_point)  # type: ignore
            self.__update_view(data_changed=data_changed, image_changed=False)

    def receive_words_and_boxes(self, words: list[str], boxes):
        if self.__active_tool is not None:
            data_changed = self.__active_tool.receive_words_and_boxes(
                words=words, boxes=boxes
            )
            self.__update_view(data_changed=data_changed, image_changed=False)

    def __draw_data(self) -> None:

        def __draw_entity_boxes(
            entity_id,
            boxes,
            color,
            width: DrawWidth,
            draw_continuity: typing.Union[None, DrawWidth] = None,
        ):
            for i, box in enumerate(boxes):
                fill = self.__toolri_settings.is_visual_option_active(
                    visual_option=VisualOptions.FILL
                )
                self.__toolri_view.image_canvas.draw_box(
                    entity_id=entity_id,
                    box=box,
                    color=color,
                    fill=fill,
                    move_dashes=False,
                    width=width,
                )
                if draw_continuity is not None and i < (len(boxes) - 1):
                    line = box_mid_right_point(boxes[i]) + box_mid_left_point(
                        boxes[i + 1]
                    )
                    self.__toolri_view.image_canvas.draw_line(
                        entity_id=entity_id,
                        line=line,
                        color=color,
                        width=draw_continuity,
                    )

        def __draw_entity_links(entity_id, links, color, width: DrawWidth):
            for link in links:

                self.__toolri_view.image_canvas.draw_link(
                    entity_id=entity_id,
                    link=link,
                    color=color,
                    move_dashes=False,
                    width=width,
                )

        # TODO: clear only updated entities for improve performance
        # clear all the canvas before new draw
        self.__toolri_view.image_canvas.delete_all_drawings()

        entities = self.__toolri_data.get_entities()
        labels = self.__toolri_settings.labels_names
        label_order = {label: index for index, label in enumerate(labels)}
        entities = sorted(
            entities,
            key=lambda entity: label_order.get(entity.label, float("inf")),
            reverse=True,
        )

        for entity in entities:
            if (
                entity.label not in labels
                and not self.__toolri_settings.is_visual_option_active(
                    VisualOptions.UNLABELED
                )
            ):
                continue
            if not self.__toolri_settings.is_label_visible(label_name=entity.label):
                continue
            color = self.__toolri_settings.get_label_color(entity.label)
            if self.__toolri_settings.box_option == BoxOptions.ENTITIES:
                boxes = [entity.box]
                child_boxes = [
                    [e.box]
                    for e in self.__toolri_data.get_child_entities_by_entity_id(
                        entity_id=entity.id
                    )
                ]
                __draw_entity_boxes(
                    entity_id=entity.id,
                    boxes=boxes,
                    width=DrawWidth.BIG,
                    color=color,
                )
            elif self.__toolri_settings.box_option == BoxOptions.WORDS:
                boxes = entity.boxes
                child_boxes = [
                    e.boxes
                    for e in self.__toolri_data.get_child_entities_by_entity_id(
                        entity_id=entity.id
                    )
                ]
                __draw_entity_boxes(
                    entity_id=entity.id,
                    boxes=boxes,
                    width=DrawWidth.BIG,
                    color=color,
                    draw_continuity=DrawWidth.MEDIUM,
                )
            elif self.__toolri_settings.box_option == BoxOptions.BOTH:
                boxes = entity.boxes
                __draw_entity_boxes(
                    entity_id=entity.id,
                    boxes=boxes,
                    width=DrawWidth.MEDIUM,
                    color=color,
                    draw_continuity=DrawWidth.SMALL,
                )
                boxes = [entity.box]
                child_boxes = [
                    [e.box]
                    for e in self.__toolri_data.get_child_entities_by_entity_id(
                        entity_id=entity.id
                    )
                ]
                __draw_entity_boxes(
                    entity_id=entity.id,
                    boxes=boxes,
                    width=DrawWidth.BIG,
                    color=color,
                )
            if self.__toolri_settings.is_visual_option_active(
                visual_option=VisualOptions.LINKS
            ):
                links = [
                    box_mid_point(boxes[0]) + box_mid_point(cb[0]) for cb in child_boxes
                ]
                __draw_entity_links(
                    entity_id=entity.id,
                    links=links,
                    width=DrawWidth.BIG,
                    color=color,
                )

    def select_active_label(self, label_name):
        self.__toolri_settings.set_active_label(label_name=label_name)

    def set_box_option(self, box_option):
        self.__toolri_settings.set_box_option(box_option)
        self.__update_view(data_changed=True, image_changed=False)

    def toggle_option_active(self, visual_option):
        self.__toolri_settings.toggle_option_active(visual_option)
        self.__update_view(data_changed=True, image_changed=False)

    def toggle_label_visibility(self, label_name: str):
        self.__toolri_settings.toggle_label_visibility(label_name)
        self.__update_view(data_changed=True, image_changed=False)

    def edit_label(self, label_name, new_label_name, label_color, label_links):
        self.__toolri_settings.edit_label(
            label_name, new_label_name, label_color, label_links
        )
        self.__toolri_data.update_label_name(
            old_label_name=label_name, new_label_name=new_label_name
        )
        self.__update_view(data_changed=True, image_changed=False, labels_changed=True)

    def create_label(self, label_name, label_color, label_links):
        if label_name not in self.settings.labels_names:
            self.__toolri_settings.create_label(label_name, label_color, label_links)
            self.__update_view(
                data_changed=True, image_changed=False, labels_changed=True
            )

    def delete_label(self, label_name):
        self.__toolri_settings.delete_label(label_name)
        self.__update_view(data_changed=True, image_changed=False, labels_changed=True)

    def get_label(self, label_name):
        return self.__toolri_settings.get_label(label_name=label_name)

    def get_labels(self):
        return self.__toolri_settings.labels

    def apply_json_data(self):
        actual_json_data = self.__toolri_data.get_json_data()
        updated_entities_ids = []
        new_json_data = self.__toolri_view.data_manager.get_json_data()
        try:
            updated_entities_ids = self.__toolri_data.set_data_by_json(
                json_data=new_json_data
            )
        except:
            pass
        self.__update_view(data_changed=True, image_changed=False)

    def clear_data(self, clear_option: typing.Literal["labels", "links", "data"]):
        if clear_option == "labels":
            self.__toolri_data.clear_all_labels()
        elif clear_option == "links":
            self.__toolri_data.clear_all_links()
        elif clear_option == "data":
            self.__toolri_data.clear_all_data()
        self.__update_view(data_changed=True, image_changed=False)

    def __activate_labels_panel(self):
        labels_names = self.__toolri_settings.labels_names
        labels_colors = [
            self.__toolri_settings.get_label_color(label) for label in labels_names
        ]
        active_label = self.__toolri_settings.active_label
        self.__toolri_view.label_picker.activate_labels_panel(
            labels_names=labels_names,
            labels_colors=labels_colors,
            active_label=active_label,
        )

    def __deactivate_labels_panel(self):
        self.__toolri_view.label_picker.deactivate_labels_panel()

    def __update_label_picker_panel(self):
        if (
            self.__active_tool is not None
            and self.__active_tool.activate_label_picker_panel
        ):
            self.__activate_labels_panel()
        else:
            self.__deactivate_labels_panel()

    def __update_view_labels_buttons(self):
        labels_names = self.__toolri_settings.labels_names
        labels_colors = [
            self.__toolri_settings.get_label_color(label_name)
            for label_name in labels_names
        ]
        labels_visibility = [
            self.__toolri_settings.is_label_visible(label_name)
            for label_name in labels_names
        ]
        self.__toolri_view.settings_manager.set_labels_buttons(
            labels_names=labels_names,
            labels_colors=labels_colors,
            labels_visibility=labels_visibility,
        )

    def __update_view_json_data(self):
        json_data = self.__toolri_data.get_json_data()
        self.__toolri_view.data_manager.set_json_data(json_data=json_data)

    def __update_view_buttons_data(self, updated_entities_ids=None):
        buttons_ids = self.__toolri_view.data_manager.get_entity_buttons_ids()
        entities_ids = self.__toolri_data.get_entities_ids()
        if updated_entities_ids is None:
            for entity_id in buttons_ids:
                if entity_id not in entities_ids:
                    self.__toolri_view.data_manager.delete_entity_button(
                        entity_id=entity_id
                    )
            for entity in self.__toolri_data.entities:
                if entity.id in buttons_ids:
                    self.__toolri_view.data_manager.update_entity_button(
                        entity_id=entity.id,
                        entity_title=entity.text,
                        color=self.__toolri_settings.get_label_color(entity.label),
                    )
                else:
                    self.__toolri_view.data_manager.add_entity_button(
                        entity_id=entity.id,
                        entity_title=entity.text,
                        color=self.__toolri_settings.get_label_color(entity.label),
                    )

    def __update_image(self):
        self.__toolri_view.image_canvas.set_image(self.__image_manager.image)

    def __update_file_names(self):
        if self.__data_file_name:
            self.__toolri_view.data_manager.set_data_file_name(self.__data_file_name)
        if self.__image_file_name:
            self.__toolri_view.data_manager.set_image_file_name(self.__image_file_name)

    def __check_data_changed(self):
        if self.__checkpoint_json_data:
            is_data_changed = (
                self.__toolri_data.get_json_data() != self.__checkpoint_json_data
            )
            self.__toolri_view.data_manager.update_save_data_button(
                is_data_changed=is_data_changed
            )

    def __update_view(
        self,
        data_changed: typing.Union[bool, list[int]],
        image_changed: bool,
        labels_changed=False,
    ):
        self.__update_file_names()
        self.__check_data_changed()
        self.__update_view_json_data()
        if image_changed:
            self.__update_image()
        if data_changed:
            self.__toolri_view.image_canvas.delete_temporary_drawings()
            self.__update_view_buttons_data()
            self.__draw_data()
        if labels_changed:
            self.__update_view_labels_buttons()
            self.__update_label_picker_panel()
            self.settings.save_settings()

    def __auto_load(self, option: typing.Literal["data", "image"]):
        if option == "data":
            if not self.__image_folder:
                self.__image_folder = self.__data_folder
            if self.__image_sample != self.__data_sample:
                for image_extension in IMAGE_FILE_EXTENSIONS:
                    image_path = (
                        f"{self.__image_folder}/{self.__data_sample}.{image_extension}"
                    )
                    if os.path.isfile(image_path):
                        self.__load_image(image_path)
        if option == "image":
            if not self.__data_folder:
                self.__data_folder = self.__image_folder
            if self.__data_sample != self.__image_sample:
                for data_extension in DATA_FILE_EXTENSIONS:
                    data_path = (
                        f"{self.__data_folder}/{self.__image_sample}.{data_extension}"
                    )
                    if os.path.isfile(data_path):
                        self.__load_data(data_path)

    def __load_image(self, image_path):
        self.__image_path = image_path
        self.__image_file_name = os.path.basename(self.__image_path)
        self.__image_sample = os.path.splitext(self.__image_file_name)[0]
        self.__image_folder = os.path.dirname(self.__image_path)
        image = PIL.Image.open(self.__image_path)
        self.__image_manager.set_image(image)
        self.__update_view(data_changed=True, image_changed=True)

    def __load_data(self, data_path):
        self.__data_path = data_path
        self.__data_file_name = os.path.basename(self.__data_path)
        self.__data_sample = os.path.splitext(self.__data_file_name)[0]
        self.__data_folder = os.path.dirname(self.__data_path)
        json_data = open(data_path).read()
        self.__toolri_data.set_data_by_json(json_data=json_data)
        self.__checkpoint_json_data = self.__toolri_data.get_json_data()
        self.__update_view(data_changed=True, image_changed=False)

    def __save_data(self, data_path):
        self.__data_path = data_path
        self.__data_file_name = os.path.basename(self.__data_path)
        self.__data_sample = os.path.splitext(self.__data_file_name)[0]
        self.__data_folder = os.path.dirname(self.__data_path)
        json_data = self.__toolri_data.get_json_data()
        with open(self.__data_path, "w") as file:
            file.write(json_data)
        self.__checkpoint_json_data = json_data
        self.__update_view(data_changed=False, image_changed=False)

    def load_image(self):
        image_path = self.__toolri_view.data_manager.open_file(
            initialdir=self.__image_folder,
            filetypes=[("Image files", OPEN_IMAGE_EXTENSIONS)],
        )
        if image_path:
            try:
                self.__load_image(image_path=image_path)
                self.__auto_load(option="image")
            except:
                pass

    def load_data(self):
        data_path = self.__toolri_view.data_manager.open_file(
            initialdir=self.__data_folder,
            filetypes=[("Data files", OPEN_DATA_EXTENSIONS)],
        )
        if data_path:
            try:
                self.__load_data(data_path=data_path)
                self.__auto_load(option="data")
            except:
                pass

    def save_data(self):
        if not self.__data_path:
            data_path = self.__toolri_view.data_manager.save_file(
                initialfile=self.__data_sample,
                defaultextension=f".{DATA_FILE_EXTENSIONS[0]}",
                initialdir=self.__data_folder,
                filetypes=[("Data files", OPEN_DATA_EXTENSIONS)],
            )
        else:
            data_path = self.__data_path
        if data_path:
            try:
                self.__save_data(data_path=data_path)
                self.__auto_load(option="data")
            except:
                pass

    def get_entity(self, entity_id: int):
        return self.__toolri_data.get_entity(entity_id=entity_id)

    def get_entities(self):
        return self.__toolri_data.get_entities()

    def get_label_color(self, label_name):
        return self.__toolri_settings.get_label_color(label_name=label_name)

    def delete_entity(self, entity_id):
        self.__toolri_data.delete_entity(entity_id=entity_id)
        self.__update_view(data_changed=[entity_id], image_changed=False)

    def edit_entity(self, entity_id, words, label):
        self.__toolri_data.edit_entity(entity_id, words, label)
        self.__update_view(data_changed=[entity_id], image_changed=False)

    def run(self):
        self.__toolri_view.run()
        self.settings.save_settings()
        data = self.__toolri_data.get_entities_dict()
        return data
