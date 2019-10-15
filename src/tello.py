import socket


class TelloState:
    def __init__(self, address="192.168.10.1", port=8890) -> None:
        self.port: int = port
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", self.port))

        self.continue_loop: bool = True
        self.recv_callback = None

    def recv_data(self) -> str:
        data, address = self.socket.recvfrom(1024)
        return str(data)

    def start(self) -> None:
        while self.continue_loop:
            data = self.recv_data()
            if self.recv_callback:
                self.recv_callback(data)


class TelloCommand:
    def __init__(self, address="192.168.10.1", port=8889) -> None:
        self.address: str = address
        self.port: int = port
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Enter SDK mode
        self.send_command("command")

    def send_command(self, command: str) -> None:
        self.socket.sendto(command.encode("UTF-8"), (self.address, self.port))

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
