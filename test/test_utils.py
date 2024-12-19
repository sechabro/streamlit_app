from utils import server_pid_terminate, server_search_and_terminate
from psutil import Process, process_iter, NoSuchProcess
from unittest.mock import patch, Mock, MagicMock, mock_open
import signal


@patch('psutil.Process')
@patch('psutil.process_iter')
def test_server_search_and_terminate(mock_process_iterable, mock_Process):
    mock_iterables = [mock_Process]
    mock_process_iterable.return_value = iter(mock_iterables)
    mock_Process.as_dict.return_value = {'pid': 1234,
                                         'name': 'Python', 'cmdline': 'script.py'}

    assert server_search_and_terminate(
        script="script.py") == ' Killed process 1234 successfully.'
    mock_Process.send_signal.assert_called_once()

    assert server_search_and_terminate(
        script=None) == f'---- Server subprocess already terminated. No PID available. ----'
    assert TypeError


@patch('os.kill')
@patch('psutil.pid_exists')
def test_pid_terminate(mock_pid_exists, mock_kill):
    mock_pid = 123
    mock_pid_exists.return_value = True
    server_pid_terminate(pid=mock_pid)
    mock_kill.assert_called_once()


@patch('os.kill')
@patch('psutil.pid_exists')
def test_pid_terminate_fail(mock_pid_exists, mock_kill):
    mock_pid = 123
    mock_pid_exists.return_value = False
    server_pid_terminate(pid=mock_pid)
    mock_kill.assert_not_called()
