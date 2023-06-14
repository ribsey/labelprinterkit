import serial

from . import BaseBackend


class BTSerialBackend(BaseBackend):
    @classmethod
    def auto(cls, dev_path: str):
        dev = serial.Serial(
            dev_path,
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
