import typing

from ...model.ocr import get_words_and_boxes_using_tesseract_OCR
from .manual import Manual

if typing.TYPE_CHECKING:
    from ...model.data import ToolRIData
    from ...view import ToolRIView
    from ..image_manager import ImageManager
    from ..settings import ToolRISettings


class OCR(Manual):

    name = "OCR"

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

    def _primary_function(self, box) -> None:
        self._box_function(box, ocr=get_words_and_boxes_using_tesseract_OCR)
