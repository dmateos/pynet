import socket
import threading

import udpserver


class TelloCommand:
    def __init__(
        self, timeout: int = 3, addr: str = "192.168.10.1", port: int = 8889
    ) -> None:
        self.address: str = addr
        self.port: int = port
        self.timeout: int = timeout

        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tello_state: udpserver.UDPServer = udpserver.UDPServer(port, self.socket)

        self.command_timeout: bool = False

        # Start receive thread to catch new messages from the tello.
        self.tello_state.recv_start()

        # Enter SDK mode
        self.command()

    def send_command(self, command: str, ignorecheck: bool = False) -> None:
        self.socket.sendto(command.encode("UTF-8"), (self.address, self.port))

        if ignorecheck:
            return

        # Use the UDPServer to poll for a return to our command and bail if
        # it takes too long.
        # Both the UDP polling and the timeout check happen in threads. (2)
        cmd_timer: threading.Timer = threading.Timer(
            self.timeout, self._command_wait_timeout_stop_loop
        )

        cmd_timer.start()
        while self.tello_state.data == udpserver.EMPTY and not self.command_timeout:
            pass
        cmd_timer.cancel()
        self.command_timeout = False

    def _command_wait_timeout_stop_loop(self) -> None:
        self.command_timeout = True
        print("command timed out")

    def command(self):
        self.send_command("command")

    def takeoff(self) -> None:
        self.send_command("takeoff")

    def land(self) -> None:
        self.send_command("land")

    def rotatec(self, x: int) -> None:
        self.send_command("cw {}".format(x))

    def rotateq(self, x: int) -> None:
        self.send_command("ccw {}".format(x))

    def forward(self, x: int) -> None:
        self.send_command("forward {}".format(x))

    def back(self, x: int) -> None:
        self.send_command("back {}".format(x))

    def left(self, x: int) -> None:
        self.send_command("left {}".format(x))

    def right(self, x: int) -> None:
        self.send_command("right {}".format(x))

    def flip(self, d: str) -> None:
        self.send_command("flip {}".format(d))

    def stop(self) -> None:
        self.send_command("stop")

    def go(self, x: int, y: int, z: int, speed: int) -> None:
        self.send_command("go {} {} {} {}".format(x, y, z, speed))

    def rc_forward(self, x: int) -> None:
        self.send_command("rc 0 {} 0 0".format(x), True)

    def rc_backward(self, x: int) -> None:
        self.send_command("rc 0 {} 0 0".format(-x), True)

    def rc_left(self, x: int) -> None:
        self.send_command("rc {} 0 0 0".format(-x), True)

    def rc_right(self, x: int) -> None:
        self.send_command("rc {} 0 0 0".format(x), True)

    def rc_up(self, x: int) -> None:
        self.send_command("rc 0 0 {} 0".format(x), True)

    def rc_down(self, x: int) -> None:
        self.send_command("rc 0 0 {} 0".format(-x), True)

    def rc_rotatec(self, x: int) -> None:
        self.send_command("rc 0 0 0 {}".format(x), True)

    def rc_rotateq(self, x: int) -> None:
        self.send_command("rc 0 0 0 {}".format(-x), True)

    def streamon(self) -> None:
        self.send_command("streamon")

    def streamoff(self) -> None:
        self.send_command("streamoff")
