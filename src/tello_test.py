from unittest.mock import patch, create_autospec
import tello
import socket


def check_sendto(command: str, socket_obj):
    socket_obj.sendto.assert_called_with(
        command.encode("UTF-8"), ("192.168.10.1", 8889)
    )


def setup_tello_command_obj(mock_socket):
    mock_socket_object = create_autospec(socket.socket)
    mock_socket.socket.return_value = mock_socket_object
    robot = tello.TelloCommand()
    return robot, mock_socket_object


def setup_tello_state_obj(mock_socket):
    mock_socket_object = create_autospec(socket.socket)
    mock_socket.socket.return_value = mock_socket_object
    state = tello.TelloState()
    return state, mock_socket_object


@patch("tello.socket", autospec=True)
def test_tello_sends_initial_sdk_command(mock_socket):
    robot, mock_socket_object = setup_tello_command_obj(mock_socket)
    check_sendto("Command", mock_socket_object)


@patch("tello.socket", autospec=True)
def test_tello_default_address_and_port_correct(mock_socket):
    robot = tello.TelloCommand()
    assert robot.address == "192.168.10.1"
    assert robot.port == 8889


@patch("tello.socket", autospec=True)
def test_tello_override_address_and_port(mock_socket):
    robot = tello.TelloCommand("192.168.10.2", 1234)
    assert robot.address == "192.168.10.2"
    assert robot.port == 1234


@patch("tello.socket", autospec=True)
def test_tello_sends_command(mock_socket):
    robot, mock_socket_object = setup_tello_command_obj(mock_socket)
    robot.send_command("test command")
    check_sendto("test command", mock_socket_object)


@patch("tello.socket", autospec=True)
def test_tello_takeoff_command(mock_socket):
    robot, mock_socket_object = setup_tello_command_obj(mock_socket)
    robot.takeoff()
    check_sendto("takeoff", mock_socket_object)


@patch("tello.socket", autospec=True)
def test_tello_land_command(mock_socket):
    robot, mock_socket_object = setup_tello_command_obj(mock_socket)
    robot.land()
    check_sendto("land", mock_socket_object)


@patch("tello.socket", autospec=True)
def test_tello_state_server(mock_socket):
    stateserver, mock_socket_object = setup_tello_state_obj(mock_socket)
    mock_socket_object.bind.assert_called_with("0.0.0.0", 8890)
