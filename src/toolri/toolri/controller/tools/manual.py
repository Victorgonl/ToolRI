import typing

from .tool import Tool

if typing.TYPE_CHECKING:
    from ...model.data import ToolRIData
    from ...view import ToolRIView
    from ..image_manager import ImageManager
    from ..settings import ToolRISettings


class Manual(Tool):

    name = "Manual"

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
            left_mouse_button_function="box",
            right_mouse_button_function="point",
        )

    def _primary_function(self, box) -> None:
        self._box_function(box)

    def _secondary_function(self, geometry_or_point: tuple[int, int]) -> list[int]:
        return self._select_function(
            point=geometry_or_point, data_function=self._toolri_data.delete_entity
        )

    def receive_words_and_boxes(self, words: list[str], boxes) -> bool:
        super().receive_words_and_boxes(words, boxes)
        if words and boxes:
            try:
                self._toolri_data.create_entity(words=words, boxes=boxes)
                self._toolri_view.words_extractor.clear()
                return True
            except:
                pass
        self._toolri_view.words_extractor.clear()
        return False
