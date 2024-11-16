import signal
import psutil
import os


class Paths:
    def __init__(self, currency, pid):
        self.datacsv = str(os.getenv('BCSV', default=None))
        self.nonstate = str(os.getenv('PIDF', default=None))
        self.currency = currency
        self.pid = pid


def server_search_and_terminate(script):
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['pid', 'name', 'cmdline'])
            if process_info["name"] == "Python" and script in process_info["cmdline"]:
                process.send_signal(signal.SIGTERM)
                return f'##### Killed process {process_info.get("pid")} successfully. #####'
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, TypeError):
            continue
    return f'##### Server subprocess already terminated. No PID available. #####'


def server_pid_terminate(pid):
    os.kill(int(pid), signal.SIGTERM)
