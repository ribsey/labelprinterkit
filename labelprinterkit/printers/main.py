from enum import Enum, auto
from typing import Type

from . import GenericPrinter
from ..constants import Resolution

class P700(GenericPrinter):
    pass


class P750W(GenericPrinter):
    pass


class H500(GenericPrinter):
    _SUPPORTED_RESOLUTIONS = (Resolution.LOW,)
    _FEATURE_HALF_CUT = False


class E500(H500):
    pass


class E550W(P750W):
    pass


class Printer(Enum):
    PTP_700 = auto()
    PTP_750W = auto()
    PTP_H500 = auto()
    PTP_E500 = auto()
    PTP_E550W = auto()

    def printer(self) -> Type[GenericPrinter]:
        match self:
            case Printer.PTP_700:
                return P700
            case Printer.PTP_750W:
                return P750W
            case Printer.PTP_H500:
                return H500
            case Printer.PTP_E500:
                return E500
            case Printer.PTP_E550W:
                return E550W
