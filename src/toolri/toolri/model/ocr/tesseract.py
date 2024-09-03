import enum

import numpy
import pytesseract


def join_boxes(boxes: list[tuple[int, int, int, int]]) -> list[int]:
    box = [0, 0, 0, 0]
    x0_list = [box[0] for box in boxes]
    y0_list = [box[1] for box in boxes]
    x1_list = [box[2] for box in boxes]
    y2_list = [box[3] for box in boxes]
    box = [min(x0_list), min(y0_list), max(x1_list), max(y2_list)]
    return box


def get_words_and_boxes_using_tesseract_OCR(image, config="-l por+eng --psm 6", conf=0):
    words = []
    boxes = []
    image_array = numpy.array(image)
    image_data = pytesseract.image_to_data(
        image_array, output_type=pytesseract.Output.DICT, config=config
    )
    n = len(image_data["text"])
    for i in range(n):
        if int(image_data["conf"][i]) > conf:
            words.append(image_data["text"][i])
            (l, t, w, h) = (
                image_data["left"][i],
                image_data["top"][i],
                image_data["width"][i],
                image_data["height"][i],
            )
            boxes.append([l, t, l + w, t + h])
    return words, boxes


def get_data_using_tesseract_OCR(image, config="-l por+eng --psm 6", conf=0):
    image_array = numpy.array(image)
    image_data = pytesseract.image_to_data(
        image_array, output_type=pytesseract.Output.DICT, config=config
    )

    data = []
    last_id = 0
    for i, text in enumerate(image_data["text"]):
        if int(image_data["conf"][i]) > conf:
            (l, t, w, h) = [
                image_data["left"][i],
                image_data["top"][i],
                image_data["width"][i],
                image_data["height"][i],
            ]
            box = [l, t, l + w, t + h]
            entity = {
                "id": last_id,
                "text": text,
                "words": [text],
                "box": box,
                "boxes": [box],
                "label": "",
                "links": [],
            }
            data.append(entity)
            last_id += 1

    return data
