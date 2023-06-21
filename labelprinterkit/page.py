from abc import ABC
from math import ceil
from typing import TypeVar, Self

from PIL import Image, ImageChops

from .constants import Resolution


def image_to_bitmap(image: Image) -> bytes:
    assert image.mode == "1"
    image = image.transpose(Image.ROTATE_270).transpose(Image.FLIP_TOP_BOTTOM)
    image = ImageChops.invert(image)
    return image.tobytes(), image.size[0], image.size[1]


class BasePage(ABC):
    _bitmap: bytes
    _height: int
    _length: int
    _resolution: Resolution

    def __init__(self):
        self.__byte_per_line = None
        assert self._byte_per_line * self.length == len(self.bitmap)

    @property
    def bitmap(self) -> bytes:
        return self._bitmap

    @property
    def height(self):
        return self._height

    @property
    def length(self):
        return self._length

    @property
    def resolution(self):
        return self._resolution

    @property
    def _byte_per_line(self):
        if self.__byte_per_line is None:
            self.__byte_per_line = ceil(self.height / 8)
        return self.__byte_per_line

    def __iter__(self):
        for i in range(0, len(self.bitmap), self._byte_per_line):
            yield self.bitmap[i:i + self._byte_per_line]


PageType = TypeVar('PageType', bound=BasePage)


class Page(BasePage):
    def __init__(self, bitmap: bytes, height: int, length: int,  resolution: Resolution = Resolution.LOW):
        self._bitmap = bitmap
        self._height = height
        self._length = length
        self._resolution = resolution
        super().__init__()

    @classmethod
    def from_image(cls, image: Image, resolution: Resolution = Resolution.LOW) -> Self:
        bitmap, height, length = image_to_bitmap(image)
        return cls(bitmap, height, length, resolution)
