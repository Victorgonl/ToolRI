import json
import os
import typing

import PIL.Image

from ..toolri.model.json import ToolRIJSONEncoder


def save_data(data, sample_name, save_folder):
    save_path = f"{save_folder}/{sample_name}.json"
    with open(save_path, "w") as data_file:
        json.dump(
            data,
            data_file,
            indent=4,
            cls=ToolRIJSONEncoder,
        )


def save_image(
    image: PIL.Image.Image,
    sample_name,
    save_folder,
    img_format: typing.Literal["png", "jpg"] = "png",
):
    save_path = f"{save_folder}/{sample_name}.{img_format}"
    image.save(save_path)


def save_sample(
    data,
    image,
    sample_name,
    dataset_folder,
    img_format: typing.Literal["png", "jpg"] = "png",
):
    image_folder = f"{dataset_folder}/image/"
    data_folder = f"{dataset_folder}/data/"
    if not os.path.isdir(image_folder):
        os.makedirs(image_folder)
    if not os.path.isdir(data_folder):
        os.makedirs(data_folder)
    save_data(data, sample_name, data_folder)
    save_image(image, sample_name, image_folder, img_format)
