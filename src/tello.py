import socket
import threading

import udpserver


class TelloCommand:
    def __init__(
        self, timeout: int = 30, address: str = "192.168.10.1", port: int = 8889
    ) -> None:
        self.address: str = address
        self.port: int = port
        self.timeout: int = timeout

        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tello_state: udpserver.UDPServer = udpserver.UDPServer(port, self.socket)
        self.timer = threading.Timer(self.timeout, self._command_wait_timeout_stop_loop)

        self.command_timeout: bool = False

        # Start receive thread to catch new messages from the tello.
        self.tello_state.recv_start()

        # Enter SDK mode
        self.send_command("command", True)

    def send_command(self, command: str, ignorecheck: bool = False) -> None:
        self.socket.sendto(command.encode("UTF-8"), (self.address, self.port))

        if not ignorecheck:
            self._command_wait_timeout()
            while self.tello_state.data == "" and not self.command_timeout:
                pass
            self.timer.cancel()
            self.command_timeout = False

    def takeoff(self) -> None:
        self.send_command("takeoff")

    def land(self) -> None:
        self.send_command("land")

    def rotate(self, x: int) -> None:
        self.send_command("cw {}".format(x))

    def forward(self, x: int) -> None:
        self.send_command("forward {}".format(x))

    def back(self, x: int) -> None:
        self.send_command("back {}".format(x))

    def left(self, x: int) -> None:
        self.send_command("left {}".format(x))

    def right(self, x: int) -> None:
        self.send_command("right {}".format(x))

    def _command_wait_timeout_stop_loop(self):
        self.command_timeout = True

    def _command_wait_timeout(self):
        self.timer.start()
