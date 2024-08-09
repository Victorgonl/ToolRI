import typing

from ...model.geometry_functions.geometry_functions import cut_image_piece, join_boxes

if typing.TYPE_CHECKING:
    from ...model.data import ToolRIData
    from ...view import ToolRIView
    from ..image_manager import ImageManager
    from ..settings import ToolRISettings


class Tool:

    name = "Tool"

    _DASH = (5,)
    _WIDTH = 2

    def __init__(
        self,
        toolri_view: "ToolRIView",
        toolri_settings: "ToolRISettings",
        toolri_image: "ImageManager",
        toolri_data: "ToolRIData",
        left_mouse_button_function: typing.Literal["point", "box", "link"] = "point",
        right_mouse_button_function: typing.Literal["point", "box", "link"] = "point",
        activate_label_picker_panel=False,
        check_for_allowed_link=True,
    ):
        self._toolri_view = toolri_view
        self._toolri_settings = toolri_settings
        self._toolri_image = toolri_image
        self._toolri_data = toolri_data

        self._toolri_view.image_canvas.delete_temporary_drawings()
        self._toolri_view.words_extractor.clear()

        self._activate_label_picker_panel = activate_label_picker_panel

        self._toolri_view.image_canvas.activate_left_mouse_button_function(
            shape=left_mouse_button_function
        )
        self._toolri_view.image_canvas.activate_right_mouse_button_function(
            shape=right_mouse_button_function
        )

        self.__check_for_allowed_link = check_for_allowed_link

    @property
    def activate_label_picker_panel(self):
        return self._activate_label_picker_panel

    def _primary_function(self, geometry_or_point) -> list[int]:
        return []

    def _secondary_function(self, geometry_or_point) -> list[int]:
        return []

    def _get_entities_by_point(self, point):
        entities = self._toolri_data.get_entities_by_point(
            point=point, box_option=self._toolri_settings.box_option
        )
        filter_entities = []
        for entity in entities:
            if self._toolri_settings.is_label_visible(entity.label):
                filter_entities.append(entity)
        return filter_entities

    def _link_function(self, geometry_or_point, data_function) -> list[int]:
        """
        Macro function when dealing with a pair of entities.
        """
        point_a = (geometry_or_point[0], geometry_or_point[1])
        point_b = (geometry_or_point[2], geometry_or_point[3])
        entities_parents = self._get_entities_by_point(point=point_a)
        entities_childs = self._get_entities_by_point(point=point_b)
        entities_modified = []
        for entity_parent in entities_parents:
            for entity_child in entities_childs:
                if (
                    self._toolri_settings.is_link_allowed(
                        entity_parent.label, entity_child.label
                    )
                    or not self.__check_for_allowed_link
                ):
                    try:
                        data_function(
                            entity_k_id=entity_parent.id,
                            entity_v_id=entity_child.id,
                        )
                        entities_modified.append(entity_parent)
                    except:
                        pass
        return entities_modified

    def _select_function(self, point, data_function):
        """
        Macro function when dealing with a single entity.
        """
        entities = self._get_entities_by_point(point=point)
        entities_modified = []
        for entity in entities:
            try:
                data_function(entity_id=entity.id)
                entities_modified.append(entity.id)
            except:
                pass
        return entities_modified

    def __adjust_box_on_image(self, box, reference_box) -> tuple[int, int, int, int]:
        new_box = (
            reference_box[0] + box[0],  # x-coordinate of the top-left corner
            reference_box[1] + box[1],  # y-coordinate of the top-left corner
            reference_box[0] + box[2],  # x-coordinate of the bottom-right corner
            reference_box[1] + box[3],  # y-coordinate of the bottom-right corner
        )
        return new_box

    def _box_function(self, box, ocr=None):
        """
        Macro function when dealing with a box selection.
        """

        def is_valid_image(image):
            size = image.size
            if size[0] == 0 or size[1] == 0:
                return False
            return True

        image_box = self._fix_box(box)
        image_piece = cut_image_piece(self._toolri_image.image, image_box)
        if is_valid_image(image_piece):
            if ocr is not None:
                words, boxes = ocr(image=image_piece)
                boxes = [self.__adjust_box_on_image(box, image_box) for box in boxes]
            else:
                words, boxes = [""], [image_box]
            if (words and boxes) or ocr is None:
                self._toolri_view.words_extractor.set_words_and_boxes(
                    words=words, boxes=boxes
                )
                box = join_boxes(boxes)
                self._toolri_view.image_canvas.draw_box(box=box, move_dashes=True)

    def _fix_box(self, box) -> tuple[int, int, int, int]:
        fixed_box = (
            min(box[0], box[2]),
            min(box[1], box[3]),
            max(box[0], box[2]),
            max(box[1], box[3]),
        )
        return fixed_box

    def select_box(self, box: tuple[int, int, int, int]) -> None:
        pass

    def select_link(self, link: tuple[int, int, int, int]):
        pass

    def select_point(self, point: tuple[int, int]) -> list[int]:
        return []

    def receive_words_and_boxes(self, words: list[str], boxes) -> list[int]:
        return []
