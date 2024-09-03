import PIL.Image

from ..toolri.model.data import EMPTY_LABEL
from ..toolri.model.ocr import get_data_using_tesseract_OCR


def create_data_by_ocr(
    image: PIL.Image.Image, conf=0, default_label=EMPTY_LABEL
) -> list[dict]:
    data = get_data_using_tesseract_OCR(image=image, conf=conf)
    for i in range(len(data)):
        data[i]["label"] = default_label
    return data
