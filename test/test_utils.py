from ..utils import server_pid_terminate, server_search_and_terminate
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

    mock_Process.send_signal(side_effect=NoSuchProcess)
    assert server_search_and_terminate(
        script="script.py") == '---- Server subprocess already terminated. No PID available. ----'
