from typing import Optional

import socket
import threading


class UDPServer:
    def __init__(
        self, port: int, supplied_socket: Optional[socket.socket] = None
    ) -> None:
        self.port: int = port
        if supplied_socket:
            sock = supplied_socket
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.socket: socket.socket = sock
        self.continue_loop: bool = True
        self.recv_thread: threading.Thread = threading.Thread(target=self._recv_loop)
        self._recvdata: str = ""

        self.socket.bind(("", self.port))

    @property
    def data(self) -> str:
        return self._recvdata

    def recv_data(self) -> str:
        data, address = self.socket.recvfrom(1024)
        if data:
            return data.decode("UTF-8")
        return ""

    def recv_start(self) -> None:
        self.recv_thread.start()

    def _recv_loop(self) -> None:
        while self.continue_loop:
            self._recvdata = self.recv_data()
