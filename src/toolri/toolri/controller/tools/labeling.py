import typing

from .tool import Tool

if typing.TYPE_CHECKING:
    from ...model.data import ToolRIData
    from ...view import ToolRIView
    from ..image_manager import ImageManager
    from ..settings import ToolRISettings


class Labeling(Tool):

    name = "Labeling"

    def __init__(
        self,
        toolri_view: "ToolRIView",
        toolri_settings: "ToolRISettings",
        toolri_image: "ImageManager",
        toolri_data: "ToolRIData",
    ):
        super().__init__(
            toolri_view=toolri_view,
            toolri_settings=toolri_settings,
            toolri_image=toolri_image,
            toolri_data=toolri_data,
        )

        self._toolri_view.image_canvas.activate_left_mouse_button_function(
            shape="point"
        )
        self._toolri_view.image_canvas.activate_right_mouse_button_function(
            shape="point"
        )
        self._activate_label_picker_panel = True

    def _primary_function(self, geometry_or_point) -> list[int]:
        entities_ids = self._toolri_data.get_entities_ids_by_point(
            image_point=geometry_or_point, box_option=self._toolri_settings.box_option
        )
        entities_modified: list[int] = []
        label = self._toolri_settings.active_label
        if label is not None:
            for entity_id in entities_ids:
                parent_entities = self._toolri_data.get_parent_entities_by_entity_id(
                    entity_id=entity_id
                )
                child_entities = self._toolri_data.get_child_entities_by_entity_id(
                    entity_id=entity_id
                )
                if all(
                    [
                        self._toolri_settings.is_link_allowed(
                            parent_entity.label, label
                        )
                        for parent_entity in parent_entities
                    ]
                ) and all(
                    [
                        self._toolri_settings.is_link_allowed(label, child_entity.label)
                        for child_entity in child_entities
                    ]
                ):
                    self._toolri_data.label_entity(entity_id=entity_id, label=label)
                    entities_modified.append(entity_id)
        return entities_modified

    def _secondary_function(self, geometry_or_point) -> list[int]:
        entities_ids = self._toolri_data.get_entities_ids_by_point(
            image_point=geometry_or_point, box_option=self._toolri_settings.box_option
        )
        entities_modified = []
        for entity_id in entities_ids:
            parent_entities = self._toolri_data.get_parent_entities_by_entity_id(
                entity_id=entity_id
            )
            child_entities = self._toolri_data.get_child_entities_by_entity_id(
                entity_id=entity_id
            )
            if not parent_entities and not child_entities:
                self._toolri_data.clear_label(entity_id=entity_id)
                entities_modified.append(entity_id)
        return entities_modified
