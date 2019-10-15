import socket


class TelloState:
    def __init__(self, address="192.168.10.1", port=8890) -> None:
        self.port: int = port
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind("0.0.0.0", self.port)


class TelloCommand:
    def __init__(self, address="192.168.10.1", port=8889) -> None:
        self.address: str = address
        self.port: int = port
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Enter SDK mode
        self.send_command("Command")

    def send_command(self, command: str) -> None:
        self.socket.sendto(command.encode("UTF-8"), (self.address, self.port))

    def takeoff(self) -> None:
        self.send_command("takeoff")

    def land(self) -> None:
        self.send_command("land")
