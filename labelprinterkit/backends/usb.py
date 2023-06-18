from typing import Self

from time import sleep

import usb.core
import usb.util

from . import BaseBackend


class PyUSBBackend(BaseBackend):
    @staticmethod
    def is_usb_printer(dev) -> bool:
        if dev.bDeviceClass == 7:
            return True
        for cfg in dev:
            if usb.util.find_descriptor(cfg, bInterfaceClass=7) is not None:
                return True

    @classmethod
    def auto(cls) -> Self:
        dev = usb.core.find(custom_match=cls.is_usb_printer)
        if dev is None:
            raise OSError('Device not found')
        return cls(dev)

    def write(self, data: bytes):
        self.dev.write(0x2, data)

    def read(self, count: int) -> bytes:
        for i in range(0, 3):
            data = self.dev.read(0x81, count)
            if data:
                return data
            sleep(0.1)