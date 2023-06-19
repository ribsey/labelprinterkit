import threading
import abc

from typing import Optional

import usb.core
import serial

class PrintingBackend(abc.ABC):
    """printing backends are responsible for transmitting and receiving the
    stream of commands from or to the printer"""

    @classmethod
    def auto(cls) -> "PrintingBackend":
        """search for printers accessible via this backend, and return a
        PrintingBackend instance. If none are found, raise OSError"""
        raise NotImplementedError()


def is_usb_printer(dev: usb.core.Device) -> bool:
    if dev.bDeviceClass == 7:
        return True
    for cfg in dev:
        if usb.util.find_descriptor(cfg, bInterfaceClass=7) is not None:
            return True
    return False


class PyUSBBackend(PrintingBackend):
    def __init__(self, dev):
        self.dev = dev

        # TODO: This does not belong here. Locking is the job of the
        # application
        self.lock = threading.Lock()

    @classmethod
    def auto(cls):
        dev = usb.core.find(custom_match=is_usb_printer)
        if dev is None:
            raise OSError('Device not found')
        return cls(dev)

    def write(self, data: bytes):
        self.dev.write(0x2, data)

    def read(self, size: Optional[int] = -1) -> bytes:
        return self.dev.read(0x81, size)

class BTSerialBackend():
    def __init__(self, dev):
        self.dev = dev
        self.lock = threading.Lock()

    @classmethod
    def auto(cls, devPath: str):
        dev = serial.Serial(
            devPath,
            baudrate=9600,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
            bytesize=8,
            dsrdtr=False,
            timeout=1
        )
        if dev is None:
            raise OSError('Device not found')
        return cls(dev)

    def write(self, data: bytes):
        self.dev.write(data)

    def read(self, count: int) -> bytes:
        data = self.dev.read(count)
        return data
