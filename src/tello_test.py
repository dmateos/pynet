from unittest.mock import patch
import tello


# TelloCommand
def _assert_socket_sendto(command: str, socket_obj):
    socket_obj.return_value.sendto.assert_called_with(
        command.encode("UTF-8"), ("192.168.10.1", 8889)
    )


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_sends_initial_sdk_command(mock_udpserver, mock_socket):
    tello.TelloCommand()
    _assert_socket_sendto("command", mock_socket)


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_default_address_and_port_correct(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    assert robot.address == "192.168.10.1"
    assert robot.port == 8889
    assert robot.timeout == 30


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_override_address_and_port_and_timeout(mock_udpserver, mock_socket):
    robot = tello.TelloCommand(1, "192.168.10.2", 1234)
    assert robot.address == "192.168.10.2"
    assert robot.port == 1234
    assert robot.timeout == 1


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_sends_command(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    robot.send_command("test command")
    _assert_socket_sendto("test command", mock_socket)


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_send_command_timeout(mock_udpserver, mock_socket):
    robot = tello.TelloCommand(1)

    # This should block for 1 second as that will
    mock_udpserver.return_value.data = ""
    robot.send_command("test command")

    mock_udpserver.return_value.recv_start.assert_called()


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_takeoff_command(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    robot.takeoff()
    _assert_socket_sendto("takeoff", mock_socket)


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_land_command(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    robot.land()
    _assert_socket_sendto("land", mock_socket)


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_rotate_command(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    robot.rotate(360)
    _assert_socket_sendto("cw {}".format(360), mock_socket)


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_forward_command(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    robot.forward(20)
    _assert_socket_sendto("forward {}".format(20), mock_socket)


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_back_command(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    robot.back(20)
    _assert_socket_sendto("back {}".format(20), mock_socket)


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_left_command(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    robot.left(20)
    _assert_socket_sendto("left {}".format(20), mock_socket)


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_right_command(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    robot.right(20)
    _assert_socket_sendto("right {}".format(20), mock_socket)


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_rc_command(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    robot.rc(5, 5, 5, 5)
    _assert_socket_sendto("rc {} {} {} {}".format(5, 5, 5, 5), mock_socket)


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_streamon_command(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    robot.streamon()
    _assert_socket_sendto("streamon", mock_socket)


@patch("tello.socket.socket", autospec=True)
@patch("tello.udpserver.UDPServer", autospec=True)
def test_tello_streamoff_command(mock_udpserver, mock_socket):
    robot = tello.TelloCommand()
    robot.streamoff()
    _assert_socket_sendto("streamoff", mock_socket)
