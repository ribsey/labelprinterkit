from time import sleep

import usb.core
import usb.util

from . import BaseBackend


class PyUSBBackend(BaseBackend):
    def __init__(self):
        dev = usb.core.find(custom_match=self.is_usb_printer)
        if dev is None:
            raise OSError('Device not found')
        self._dev = dev

    @staticmethod
    def is_usb_printer(dev) -> bool:
        if dev.bDeviceClass == 7:
            return True
        for cfg in dev:
            if usb.util.find_descriptor(cfg, bInterfaceClass=7) is not None:
                return True

    def write(self, data: bytes):
        self._dev.write(0x2, data)

    def read(self, count: int) -> bytes:
        for i in range(0, 3):
            data = self._dev.read(0x81, count)
            if data:
                return data
            sleep(0.1)
