from typing import Optional

import socket
import threading

EMPTY = ""


class UDPServer:
    def __init__(
        self, port: int, supplied_socket: Optional[socket.socket] = None
    ) -> None:
        self.port: int = port

        # Optionally use a user supplied socket
        if supplied_socket:
            sock = supplied_socket
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.socket: socket.socket = sock
        self._recvdata: str = EMPTY

        # We run the the receiver in a thread until asked to stop.
        self.continue_loop: bool = True
        self.recv_thread: threading.Thread = threading.Thread(target=self._recv_loop)

        self.socket.bind(("", self.port))

    @property
    def data(self) -> str:
        d: str = self._recvdata
        self._recvdata = EMPTY
        return d

    def recv_data(self) -> str:
        data, address = self.socket.recvfrom(1024)
        if data:
            print("data is {}".format(data))
            return data.decode("UTF-8")
        return EMPTY

    def recv_start(self) -> None:
        self.recv_thread.start()

    def _recv_loop(self) -> None:
        while self.continue_loop:
            self._recvdata = self.recv_data()
