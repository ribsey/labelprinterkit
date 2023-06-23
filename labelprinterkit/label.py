from abc import ABC, abstractmethod
from logging import getLogger
from math import ceil
from typing import TypeVar, NamedTuple

from PIL import Image, ImageChops, ImageDraw, ImageFont

from .constants import Resolution
from .page import BasePage, image_to_bitmap

logger = getLogger(__name__)


def crop(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    else:
        return im


class Padding(NamedTuple):
    left: int
    top: int
    bottom: int
    right: int


class Item(ABC):
    @abstractmethod
    def render(self, height: int) -> Image:
        ...


ItemType = TypeVar('ItemType', bound=Item)


class Text(Item):
    def __init__(self, text: str, font_path: str, font_index: int = 0, font_size: int | None = None,
            padding: Padding = Padding(0, 0, 0, 0)):
        self.text = text
        self.font_path = font_path
        self.font_index = font_index
        self.font_size = font_size

        if any([i < 0 for i in padding]):
            raise ValueError("Negative padding is not supported: {padding}")
        self.padding = padding

    def render(self, height: int) -> Image:
        iheight = height - self.padding.top - self.padding.bottom
        if self.font_size is None:
            font_size = self._calc_font_size(iheight)
            logger.debug(f"text: {self.text}, calculated font size: {font_size}")
        else:
            font_size = self.font_size
        font = ImageFont.truetype(self.font_path, font_size, self.font_index)
        text_x, text_y = font.getsize(self.text)
        padded_size = (
            text_x + self.padding.left + self.padding.right,
            text_y + self.padding.top + self.padding.bottom,
        )

        image = Image.new("1", padded_size, "white")
        fimage = Image.new("1", font.getsize(self.text), "white")
        draw = ImageDraw.Draw(fimage)
        draw.text((0, 0), self.text, "black", font)
        fimage = crop(fimage)
        image.paste(fimage, (self.padding.left, self.padding.top))
        return image

    def _calc_font_size(self, height: int) -> int:
        lower = 1
        upper = 1
        while True:
            font = ImageFont.truetype(self.font_path, upper)
            image = Image.new("1", font.getsize(self.text), "white")
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), self.text, "black", font)
            font_height = crop(image).size[1]
            if font_height >= height:
                break
            lower = upper
            upper *= 2
        while True:
            test = ceil((upper+lower)/2)
            font = ImageFont.truetype(self.font_path, test)
            image = Image.new("1", font.getsize(self.text), "white")
            draw = ImageDraw.Draw(image)
            draw.text((0, 0), self.text, "black", font)
            font_height = crop(image).size[1]
            if upper - lower <= 1:
                return lower
            elif font_height > height:
                upper = test
            elif font_height < height:
                lower = test
            else:
                return test


class Row:
    def __init__(self, height: int, *items: ItemType):
        self.height = height
        self.length = 0
        self.items = items

    def render(self) -> Image:
        rendered_images = [item.render(self.height) for item in self.items]
        length = sum([rendered_image.size[0] for rendered_image in rendered_images])
        image = Image.new("1", (length, self.height), "white")
        ypos = 0
        for rendered_image in rendered_images:
            image.paste(rendered_image, (ypos, 0))
            ypos += rendered_image.size[0]
        return image


class Label(BasePage):
    def __init__(self, *rows: Row):
        self.rows = rows

        rendered_images = [row.render() for row in self.rows]
        length = max([rendered_image.size[0] for rendered_image in rendered_images])
        width = sum([rendered_image.size[1] for rendered_image in rendered_images])
        image = Image.new("1", (length, width), "white")
        xpos = 0
        for rendered_image in rendered_images:
            image.paste(rendered_image, (0, xpos))
            xpos += rendered_image.size[1]
        self._bitmap, self._width , self._length = image_to_bitmap(image)
        self._resolution = Resolution.LOW

        logger.debug(f"label width {self._width}")
        logger.debug(f"label length {self._length}")

        super().__init__()
