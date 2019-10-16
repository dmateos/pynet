from unittest.mock import patch, Mock
import udpserver


# UDPServer
def _setup_udpserver(mock_socket):
    mock_socket.return_value.recvfrom.return_value = (
        "test data".encode("UTF-8"),
        "127.0.0.1",
    )

    server = udpserver.UDPServer(8889)
    return server


@patch("udpserver.socket.socket", autospec=True)
def test_udpserver_server_binds_to_socket(mock_socket):
    _setup_udpserver(mock_socket)
    mock_socket.return_value.bind.assert_called_with(("", 8889))


def test_udpserver_binds_to_supplied_socket():
    test_socket = Mock()
    udpserver.UDPServer(8889, test_socket)
    test_socket.bind.assert_called_with(("", 8889))


@patch("udpserver.socket.socket", autospec=True)
def test_udpserver_recieves_data(mock_socket):
    stateserver = _setup_udpserver(mock_socket)

    data = stateserver.recv_data()

    mock_socket.return_value.recvfrom.assert_called()
    assert data == "test data"


@patch("udpserver.socket.socket", autospec=True)
def test_udpserver_runs_recv_loop_thread_and_stops(mock_socket):
    stateserver = _setup_udpserver(mock_socket)

    # This test will block ending if the loop stopping logic isnt working.
    stateserver.recv_start()
    stateserver.continue_loop = False

    mock_socket.return_value.recvfrom.assert_called()


@patch("udpserver.socket.socket", autospec=True)
def test_udpserver_state_recv_loop_sets_returned_data_property(mock_socket):
    stateserver = _setup_udpserver(mock_socket)

    stateserver.recv_start()
    stateserver.continue_loop = False

    assert stateserver.data == "test data"
