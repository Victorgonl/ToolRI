import numpy
import pytesseract


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
