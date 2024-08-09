import typing

from .tool import Tool

if typing.TYPE_CHECKING:
    from ...model.data import ToolRIData
    from ...view import ToolRIView
    from ..image_manager import ImageManager
    from ..settings import ToolRISettings


class Linking(Tool):

    name = "Linking"

    _DASH = (5,)
    _WIDTH = 2

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
            left_mouse_button_function="link",
            right_mouse_button_function="point",
        )

    def _primary_function(self, geometry_or_point) -> list[int]:
        return self._link_function(
            geometry_or_point=geometry_or_point,
            data_function=self._toolri_data.link_entities,
        )

    def _secondary_function(self, geometry_or_point) -> list[int]:
        return self._select_function(
            point=geometry_or_point, data_function=self._toolri_data.clear_links
        )
