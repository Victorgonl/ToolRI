import numpy
import PIL.Image


def cut_image_piece(image, box):
    image_array = numpy.array(image)
    x1, y1, x2, y2 = box
    image_piece = PIL.Image.fromarray(image_array[y1:y2, x1:x2])
    return image_piece


def join_boxes(boxes: list[tuple[int, int, int, int]]) -> tuple[int, int, int, int]:
    box = [0, 0, 0, 0]
    x0_list = [box[0] for box in boxes]
    y0_list = [box[1] for box in boxes]
    x1_list = [box[2] for box in boxes]
    y2_list = [box[3] for box in boxes]
    box = (min(x0_list), min(y0_list), max(x1_list), max(y2_list))
    return box


def box_mid_point(box: tuple[int, int, int, int]) -> tuple[int, int]:
    x = (box[0] + box[2]) // 2
    y = (box[1] + box[3]) // 2
    return (x, y)


def box_mid_left_point(box: tuple[int, int, int, int]) -> tuple[int, int]:
    point = (box[0], (box[1] + box[3]) // 2)
    return point


def box_mid_right_point(box: tuple[int, int, int, int]) -> tuple[int, int]:
    point = (box[2], (box[1] + box[3]) // 2)
    return point
