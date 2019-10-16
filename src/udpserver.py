import socket
import threading


class UDPServer:
    def __init__(self, port: int, supplied_socket: socket.socket = None) -> None:
        self.port: int = port
        if supplied_socket:
            self.socket = supplied_socket
        else:
            self.socket: socket.socket = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM
            )
        self.socket.bind(("", self.port))

        self.continue_loop: bool = True
        self.recv_thread: threading.Thread = threading.Thread(target=self._recv_loop)
        self._recvdata: str = ""

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
