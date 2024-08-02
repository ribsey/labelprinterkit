from enum import Enum, auto
from typing import Type

from labelprinterkit.backends import BaseBackend
from labelprinterkit.backends.bluetooth import BTSerialBackend
from labelprinterkit.backends.network import NetworkBackend
from labelprinterkit.backends.usb import PyUSBBackend

class ConnectionType(Enum):
    USB = auto()
    WIFI = auto()
    BLUETOOTH = auto()

    @property
    def backend(self) -> Type[BaseBackend]:
        match self:
            case ConnectionType.USB:
                return PyUSBBackend
            case ConnectionType.BLUETOOTH:
                return BTSerialBackend
            case ConnectionType.WIFI:
                return NetworkBackend

    @staticmethod
    def get(name: str) -> "ConnectionType":
        for connection_type in ConnectionType:
            if connection_type.name.lower() == name.lower():
                return connection_type
        raise ValueError(f"Backend with name {name} not found")
