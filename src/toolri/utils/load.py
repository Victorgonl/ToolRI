import json

import PIL.Image


def load_data(data_path):
    with open(data_path) as data_file:
        data = json.load(data_file)
    return data


def load_image(image_path):
    image = PIL.Image.open(image_path)
    image = image.convert("RGB")
    return image
