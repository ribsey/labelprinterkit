from abc import ABC, abstractmethod
import threading


class BaseBackend(ABC):
    def __init__(self, dev):
        self.dev = dev

        # TODO: This does not belong here. Locking is the job of the
        # application
        self.lock = threading.Lock()

    @abstractmethod
    def write(self, data: bytes):
        ...

    @abstractmethod
    def read(self, count: int) -> bytes:
        ...
