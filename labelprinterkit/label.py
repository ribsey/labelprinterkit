"""
Labels are the Base class you derive your Labels from.
"""
from typing import Tuple
from logging import getLogger

from PIL import Image, ImageChops, ImageDraw, ImageFont

from .page import Page

logger = getLogger(__name__)


def _coord_add(tup1, tup2):
    """add two tuples of size two"""
    return tup1[0] + tup2[0], tup1[1] + tup2[1]


class Text:
    """A simple text item"""
    def __init__(self, font: ImageFont = None, **kwargs) -> None:
        if font:
            self.font = font
        else:
            # fallback to default font
            self.font = ImageFont.load_default()

        self.pad_top = kwargs.get("pad_top", 0)
        self.pad_right = kwargs.get("pad_right", 0)
        self.pad_bottom = kwargs.get("pad_bottom", 0)
        self.pad_left = kwargs.get("pad_left", 0)

    def render(self, text):
        text_x, text_y = self.font.getsize(text)
        padded_size = (
            text_x + self.pad_left + self.pad_right,
            text_y + self.pad_top + self.pad_bottom,
        )
        image = Image.new("1", padded_size, "white")
        draw = ImageDraw.Draw(image)
        draw.text((self.pad_left, self.pad_top), text, "black", self.font)
        return image


class Label:
    """Base class for all labels

    >>> class MyLabel(Label):
    ...     items = [
    ...         [Text(), Text()],
    ...         [Text()]
    ...     ]
    >>> label = MyLabel("text1", "text2")
    >>> printer.print(label)

    """
    items = []  # type: list

    def __init__(self, *args):
        if not self.items:
            raise ValueError(
                "A Labels 'items' attribute must contain a list of "
                "renderable objects")

        arg_it = iter(args)
        try:
            self._rendered_items = [
                [item.render(next(arg_it)) for item in line]
                for line in self.items]
        except StopIteration:
            # the argument list was exhausted before all items had a value
            raise TypeError("{cls} requires {argc} arguments, but {num} were given".format(
                cls=self.__class__.__name__, argc=sum(len(x) for x in self.items), num=len(args)
            ))

    @property
    def size(self) -> Tuple[int, int]:
        width = max(sum(i.size[0] for i in line)
                    for line in self._rendered_items)
        height = sum(max(i.size[1] for i in line)
                     for line in self._rendered_items)

        return width, height

    def render(self, height=None) -> Image:
        """render the Label.

        Args:
            height: Height request
        """
        size = self.size
        img = Image.new("1", size, "white")

        pos = [0, 0]

        for line in self._rendered_items:
            for item in line:
                box = (*pos, *_coord_add(item.size, pos))
                img.paste(item, box=box)
                pos[0] += item.size[0]

            pos[0] = 0
            pos[1] += max(i.size[1] for i in line)

        xdim, ydim = img.size
        logger.debug(f"presize {xdim}, {ydim}, {height}")
        xdim = round((height / ydim) * xdim)

        logger.debug(f"calcsize {xdim}, {ydim}")
        img = img.resize((xdim, height))

        return img

    def page(self, height: int):
        img = self.render(height=height)
        if not img.mode == "1":
            raise ValueError("render output has invalid mode '1'")
        img = img.transpose(Image.ROTATE_270).transpose(
            Image.FLIP_TOP_BOTTOM)
        img = ImageChops.invert(img)
        page = Page(img.tobytes(), img.size[0], img.size[1])
        return page
