from abc import ABC
from math import ceil
from typing import TypeVar

from .constants import Resolution


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
