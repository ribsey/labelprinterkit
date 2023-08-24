from __future__ import annotations
from pkg_resources import get_distribution

__all__ = ["printers", "backends", "label", "job", "page"]
__version__ = get_distribution(__name__).version
