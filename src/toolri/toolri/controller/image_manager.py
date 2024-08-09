import typing

import PIL.Image


class ImageManager:

    EMPTY_IMAGE = PIL.Image.new("RGBA", (100, 100), (0, 0, 0, 0))

    def __init__(self, image: typing.Union[None, PIL.Image.Image]) -> None:
        if image is None:
            image = self.EMPTY_IMAGE
        self.__image = image

    @property
    def image(self):
        return self.__image

    @property
    def width(self):
        return self.__image.size[0]

    @property
    def height(self):
        return self.__image.size[1]

    def set_image(self, image: PIL.Image.Image):
        self.__image = image
