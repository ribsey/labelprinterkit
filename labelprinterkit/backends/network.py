import socket

from . import BaseBackend


class TCPBackend(BaseBackend):
    def __init__(self, host, port=9100, timeout = 10):
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
        except (socket.gaierror, ConnectionError):
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((host, port))
            except (socket.gaierror, ConnectionError):
                raise ConnectionError(f"Connection to {host} failed.")
        self._sock = sock

    def write(self, data: bytes) -> None:
        sent = self._sock.send(data)
        if sent == 0:
            raise IOError("Socket connection broken")
