from unittest.mock import patch, create_autospec
import tello
import socket


# TelloCommand
def _assert_socket_sendto(command: str, socket_obj):
    socket_obj.sendto.assert_called_with(
        command.encode("UTF-8"), ("192.168.10.1", 8889)
    )


def _setup_tello_command_obj(mock_socket):
    mock_socket_object = create_autospec(socket.socket)
    mock_socket.socket.return_value = mock_socket_object
    robot = tello.TelloCommand()
    return robot, mock_socket_object


@patch("tello.socket", autospec=True)
@patch("tello.TelloState", autospec=True)
def test_tello_sends_initial_sdk_command(mock_tellostate, mock_socket):
    robot, mock_socket_object = _setup_tello_command_obj(mock_socket)
    _assert_socket_sendto("command", mock_socket_object)


@patch("tello.socket", autospec=True)
@patch("tello.TelloState", autospec=True)
def test_tello_default_address_and_port_correct(mock_tellostate, mock_socket):
    robot = tello.TelloCommand()
    assert robot.address == "192.168.10.1"
    assert robot.port == 8889


@patch("tello.socket", autospec=True)
@patch("tello.TelloState", autospec=True)
def test_tello_override_address_and_port(mock_tellostate, mock_socket):
    robot = tello.TelloCommand("192.168.10.2", 1234)
    assert robot.address == "192.168.10.2"
    assert robot.port == 1234


@patch("tello.socket", autospec=True)
@patch("tello.TelloState", autospec=True)
def test_tello_sends_command(mock_tellostate, mock_socket):
    robot, mock_socket_object = _setup_tello_command_obj(mock_socket)
    robot.send_command("test command")
    _assert_socket_sendto("test command", mock_socket_object)


@patch("tello.socket", autospec=True)
@patch("tello.TelloState", autospec=True)
def test_tello_takeoff_command(mock_tellostate, mock_socket):
    robot, mock_socket_object = _setup_tello_command_obj(mock_socket)
    robot.takeoff()
    _assert_socket_sendto("takeoff", mock_socket_object)


@patch("tello.socket", autospec=True)
@patch("tello.TelloState", autospec=True)
def test_tello_land_command(mock_tellostate, mock_socket):
    robot, mock_socket_object = _setup_tello_command_obj(mock_socket)
    robot.land()
    _assert_socket_sendto("land", mock_socket_object)


@patch("tello.socket", autospec=True)
@patch("tello.TelloState", autospec=True)
def test_tello_rotate_command(mock_tellostate, mock_socket):
    robot, mock_socket_object = _setup_tello_command_obj(mock_socket)
    robot.rotate(360)
    _assert_socket_sendto("cw {}".format(360), mock_socket_object)


@patch("tello.socket", autospec=True)
@patch("tello.TelloState", autospec=True)
def test_tello_forward_command(mock_tellostate, mock_socket):
    robot, mock_socket_object = _setup_tello_command_obj(mock_socket)
    robot.forward(20)
    _assert_socket_sendto("forward {}".format(20), mock_socket_object)


@patch("tello.socket", autospec=True)
@patch("tello.TelloState", autospec=True)
def test_tello_back_command(mock_tellostate, mock_socket):
    robot, mock_socket_object = _setup_tello_command_obj(mock_socket)
    robot.back(20)
    _assert_socket_sendto("back {}".format(20), mock_socket_object)


@patch("tello.socket", autospec=True)
@patch("tello.TelloState", autospec=True)
def test_tello_left_command(mock_tellostate, mock_socket):
    robot, mock_socket_object = _setup_tello_command_obj(mock_socket)
    robot.left(20)
    _assert_socket_sendto("left {}".format(20), mock_socket_object)


@patch("tello.socket", autospec=True)
@patch("tello.TelloState", autospec=True)
def test_tello_right_command(mock_tellostate, mock_socket):
    robot, mock_socket_object = _setup_tello_command_obj(mock_socket)
    robot.right(20)
    _assert_socket_sendto("right {}".format(20), mock_socket_object)


# TelloState
def _setup_tello_state_obj(mock_socket):
    mock_socket_object = create_autospec(socket.socket)

    mock_socket_object.recvfrom.return_value = (
        "test data".encode("UTF-8"),
        "127.0.0.1",
    )
    mock_socket.socket.return_value = mock_socket_object

    state = tello.TelloState(8889)
    return state, mock_socket_object


@patch("tello.socket", autospec=True)
def test_tello_state_server(mock_socket):
    stateserver, mock_socket_object = _setup_tello_state_obj(mock_socket)
    mock_socket_object.bind.assert_called_with(("", 8889))


@patch("tello.socket", autospec=True)
def test_tello_state_recieves_data(mock_socket):
    stateserver, mock_socket_object = _setup_tello_state_obj(mock_socket)

    data = stateserver.recv_data()

    mock_socket_object.recvfrom.assert_called()
    assert data == "test data"


@patch("tello.socket", autospec=True)
def test_tello_state_runs_recv_loop_thread(mock_socket):
    stateserver, mock_socket_object = _setup_tello_state_obj(mock_socket)

    # This test will block ending if the loop stopping logic isnt working.
    stateserver.recv_start()
    stateserver.continue_loop = False

    mock_socket_object.recvfrom.assert_called()


@patch("tello.socket", autospec=True)
def test_tello_state_recv_loop_sets_returned_data_property(mock_socket):
    stateserver, mock_socket_object = _setup_tello_state_obj(mock_socket)

    stateserver.recv_start()
    stateserver.continue_loop = False

    assert stateserver.data == "test data"
