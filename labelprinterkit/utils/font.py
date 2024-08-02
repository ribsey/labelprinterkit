import os
from pathlib import Path
from typing import NewType

FontPath = NewType("FontPath", Path)


LINUX_TRUETYPE_FONT_DIRECTORY = "/usr/share/fonts/truetype"


def get_linux_fonts() -> dict[str, list[FontPath]]:
    """Get all Paths to Linux Fonts : Dict with Key as the Font Name and Value as a List of Paths of Font Variants"""
    fonts = {}
    for font in os.listdir(LINUX_TRUETYPE_FONT_DIRECTORY):
        fonts[font] = []
        for font_variant in os.listdir(f"{LINUX_TRUETYPE_FONT_DIRECTORY}/{font}"):
            fonts[font].append(FontPath(Path(f"{LINUX_TRUETYPE_FONT_DIRECTORY}/{font}/{font_variant}")))
    return fonts
