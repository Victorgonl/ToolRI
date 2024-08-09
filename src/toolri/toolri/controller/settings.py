from __future__ import annotations

import dataclasses
import enum
import json
import os
import sys
import typing

from ..model.data import EMPTY_LABEL, BoxOptions
from ..model.json.json_encoder import ToolRIJSONEncoder


class ToolRIInstance(enum.Enum):
    BINARY = "binary"
    PACKAGE = "package"


class VisualOptions(str, enum.Enum):
    UNLABELED = "Unlabeled"
    LINKS = "Links"
    FILL = "Fill"


@dataclasses.dataclass
class ToolRILabel:
    name: str
    color: str
    links: list[str]
    is_visible: bool


class ToolRISettings:

    __DEFAULT_SETTINGS = {
        "labels": [
            {
                "name": "HEADER",
                "color": "#F6A800",
                "links": ["HEADER", "QUESTION", "ANSWER"],
                "is_visible": True,
            },
            {
                "name": "QUESTION",
                "color": "#004B80",
                "links": ["ANSWER"],
                "is_visible": True,
            },
            {
                "name": "ANSWER",
                "color": "#00943E",
                "links": [],
                "is_visible": True,
            },
            {
                "name": "OTHER",
                "color": "#DE1F26",
                "links": [],
                "is_visible": True,
            },
        ]
    }
    __SETTINGS_FILE = "ToolRI-Settings.json"

    def __init__(
        self,
        toolri_instance: ToolRIInstance,
        labels: typing.Union[None, list[ToolRILabel]],
    ) -> None:
        self.__toolri_instance = toolri_instance
        self.__labels: dict[str, ToolRILabel] = {}
        self.__box_option = BoxOptions.ENTITIES
        self.__visual_option = {visual_option: True for visual_option in VisualOptions}
        self.__active_label = EMPTY_LABEL

        if self.__toolri_instance == ToolRIInstance.BINARY:
            self.__read_settings_file()
        else:
            if labels is None:
                settings_json = self.__DEFAULT_SETTINGS
            else:
                settings_json = {"labels": [label.__dict__ for label in labels]}
            self.__set_settings(settings_json=settings_json)

    def save_settings(self):
        if self.__toolri_instance == ToolRIInstance.BINARY:
            if getattr(sys, "frozen", False):
                application_path = os.path.dirname(sys.executable)
            elif __file__:
                application_path = os.path.dirname(__file__)

            config_path = os.path.join(application_path, self.__SETTINGS_FILE)

            with open(config_path, "w") as config_file:
                settings = {
                    "labels": [label.__dict__ for label in self.__labels.values()]
                }
                json.dump(settings, config_file, indent=4, cls=ToolRIJSONEncoder)

    def __read_settings_file(self):
        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)
        config_path = os.path.join(application_path, self.__SETTINGS_FILE)
        if os.path.exists(config_path):
            with open(config_path, "r") as config_file:
                settings = json.load(config_file)
        else:
            settings = self.__DEFAULT_SETTINGS
        self.__set_settings(settings)
        self.save_settings()

    def __set_settings(self, settings_json):
        self.__set_labels(labels_dict=settings_json["labels"])

    def __set_labels(self, labels_dict):
        self.__labels = {
            label["name"]: ToolRILabel(
                name=label["name"],
                color=label["color"],
                links=label["links"],
                is_visible=label["is_visible"],
            )
            for label in labels_dict
        }
        self.update()

    def is_label_visible(self, label_name: str) -> bool:
        if label_name not in self.__labels:
            return True
        return self.__labels[label_name].is_visible

    def get_label_color(self, label_name: str) -> str:
        if label_name not in self.__labels:
            return "#000000"
        return self.__labels[label_name].color

    def is_link_allowed(self, parent_entity_label, child_entity_label) -> bool:
        if (
            parent_entity_label not in self.__labels
            or child_entity_label not in self.__labels
        ):
            return False
        return child_entity_label in self.__labels[parent_entity_label].links

    def set_active_label(self, label_name: str):
        if label_name in self.__labels:
            self.__active_label = label_name

    def set_box_option(self, box_option: BoxOptions):
        self.__box_option = box_option

    def is_visual_option_active(self, visual_option: VisualOptions):
        return self.__visual_option[visual_option]

    def toggle_option_active(self, visual_option: VisualOptions):
        self.__visual_option[visual_option] = not self.__visual_option[visual_option]

    def toggle_label_visibility(self, label_name: str):
        self.__labels[label_name].is_visible = not self.__labels[label_name].is_visible

    def get_label(self, label_name):
        return self.__labels[label_name]

    def edit_label(self, current_label_name, new_label_name, label_color, label_links):
        new_labels: dict[str, ToolRILabel] = {}
        for label in self.__labels.values():
            if label.name == current_label_name:
                label.name = new_label_name
                label.color = label_color
                label.links = label_links
                label.is_visible = True
            if current_label_name in label.links:
                label.links.remove(current_label_name)
                label.links.append(new_label_name)
            new_labels[label.name] = label
        self.__labels = new_labels
        self.update()

    def create_label(self, label_name, label_color, label_links):
        new_label = ToolRILabel(
            name=label_name, color=label_color, is_visible=True, links=label_links
        )
        self.__labels[new_label.name] = new_label
        self.update()

    def delete_label(self, label_name):
        del self.__labels[label_name]
        if self.active_label == label_name:
            self.__active_label = None
        self.update()

    @property
    def active_label(self):
        return self.__active_label

    @property
    def labels_names(self):
        return list(self.__labels.keys())

    @property
    def labels(self):
        return list(self.__labels.values())

    @property
    def box_option(self):
        return self.__box_option

    @property
    def instance(self):
        return self.__toolri_instance

    def update(self):
        if self.__active_label == EMPTY_LABEL and self.__labels:
            self.__active_label = list(self.__labels.keys())[0]
