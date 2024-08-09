import math
import typing

import PIL.Image
import PIL.ImageDraw

from ..toolri.controller import ToolRILabel

BLACK = "#000000"
WHITE = "#FFFFFF"


def get_labels(data):
    labels = set()
    for d in data:
        label = d["label"]
        labels.add(label)
    return list(labels)


def box_mid_point(box):
    x = (box[0] + box[2]) // 2
    y = (box[1] + box[3]) // 2
    return [x, y]


def hex_to_rgb(hex_color, alpha_percent=None):
    """
    Convert a hexadecimal color to an RGB or RGBA tuple.

    Parameters:
    hex_color (str): The hexadecimal color code (e.g., "#000000").
    alpha_percent (float, optional): The alpha value as a percentage (0-100). Defaults to None.

    Returns:
    tuple: A tuple representing the RGB or RGBA color.
    """
    # Remove the hash symbol if present
    hex_color = hex_color.lstrip("#")

    # Convert hex to RGB
    rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    # Convert alpha percentage to a value between 0 and 255
    if alpha_percent is not None:
        alpha = int((alpha_percent / 100) * 255)
        return rgb + (alpha,)
    else:
        return rgb


def draw_arrow_on_image(
    image_draw, line, width=1, outline_width=1.5, color=(0, 0, 0), outline_color=None
):

    head_size = round(width * 1.25)
    head_width = round(width * 3)

    x = 1 - head_width / line_length(line)

    x0, y0 = line[0]
    x1, y1 = line[1]

    xb = x * (x1 - x0) + x0
    yb = x * (y1 - y0) + y0

    alpha = math.atan2(y1 - y0, x1 - x0) - 90.0 * math.pi / 180.0
    a = head_size * math.cos(alpha)
    b = head_size * math.sin(alpha)
    vtx0 = (xb + a, yb + b)
    vtx1 = (xb - a, yb - b)

    image_draw.polygon(
        [vtx0, vtx1, line[1]],
        fill=color,
        outline=outline_color,
        width=round((outline_width / 10) * width),
    )

    base_line = shorten_line(line, x=x)

    if outline_color is not None:
        image_draw.line(
            base_line, width=round(width * (outline_width / 2)), fill=outline_color
        )
    image_draw.line(base_line, width=width, fill=color)


def line_length(line):
    x0, y0 = line[0]
    x1, y1 = line[1]
    return math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)


def shorten_line(line, x):
    x0, y0 = line[0]
    x1, y1 = line[1]
    dx = x1 - x0
    dy = y1 - y0
    return [(x0, y0), (x0 + x * dx, y0 + x * dy)]


def draw_data_on_image(
    image,
    data,
    labels: typing.Union[None, list[ToolRILabel]] = None,
    draw_links=True,
    labels_color=True,
    links_color=True,
    box_outline_width=None,
    box_outline_color="black",
    fill_color_alpha=38.0,
    links_color_alpha=38.0,
    draw_arrow=True,
):
    # line
    line_width = round((1 / 1000) * image.size[0])
    if box_outline_width is None:
        box_outline_width = line_width + round(5 / 10 * line_width)
    # image
    image = image.copy().convert("RGBA")
    image_boxes = PIL.Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = PIL.ImageDraw.Draw(image_boxes)
    # label2color
    label2color = {}
    if labels is not None:
        for label in labels:
            label2color[label.name] = label.color
    #
    boxes_per_color = {}
    for color in label2color.values():
        boxes_per_color[color] = []
    for i in range(len(data)):
        box = data[i]["box"]
        id = data[i]["id"]
        links = data[i]["links"]
        label = data[i]["label"]
        if labels_color:
            if label not in label2color:
                color = BLACK
            else:
                color = label2color[label]
        else:
            color = WHITE
        if color not in boxes_per_color:
            boxes_per_color[color] = []
        boxes_per_color[color].append(box)
    for color in boxes_per_color.keys():
        for box in boxes_per_color[color]:
            fill = hex_to_rgb(color, fill_color_alpha)
            draw.rectangle(
                box,
                fill=fill,
                outline=box_outline_color,
                width=box_outline_width,
            )
    if draw_links:
        links = []
        for entity in data:
            for link in entity["links"]:
                if link not in links:
                    links.append(link)
        links = sorted(links, key=lambda link: link[0])
        labels = []
        lines = []
        for link in links:
            p_1, p_2 = (0, 0), (0, 0)
            color = (0, 0, 0)
            for entity in data:
                if entity["id"] == link[0]:
                    p_1 = box_mid_point(entity["box"])
                    label = entity["label"]
                    for entity in data:
                        if entity["id"] == link[1]:
                            p_2 = box_mid_point(entity["box"])
                            line = (tuple(p_1), tuple(p_2))
                            labels.append(label)
                            lines.append(line)
                            break
                    break
        for label in label2color:
            if links_color:
                color = label2color[label]
            else:
                color = BLACK
            color = hex_to_rgb(color, links_color_alpha)
            for line_label, line in zip(labels, lines):
                if line_label == label:
                    if draw_arrow:
                        draw_arrow_on_image(
                            image_draw=draw,
                            line=line,
                            width=4 * line_width,
                            outline_width=box_outline_width,
                            color=color,
                            outline_color=(0, 0, 0),
                        )
                    else:
                        draw.line(line, fill=hex_to_rgb(BLACK), width=4 * line_width)
                        draw.line(line, fill=color, width=3 * line_width)
    image_boxes = PIL.Image.alpha_composite(image, image_boxes)
    return image_boxes
