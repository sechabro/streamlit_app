import signal
import psutil
import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def server_search_and_terminate(script=None):
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['pid', 'name', 'cmdline'])
            if process_info["name"] == "Python" and script in process_info["cmdline"]:
                process.send_signal(signal.SIGTERM)
                return f' Killed process {process_info.get("pid")} successfully.'
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, TypeError):
            continue
    return f'---- No server subprocess to terminate. Server has either already been terminated, or the app is running for the first time. ----'


def server_pid_terminate(pid):
    if psutil.pid_exists(int(pid)):
        logger.info(f"Killing pid {pid}.")
        os.kill(int(pid), signal.SIGTERM)
    else:
        logger.info(f"pid {pid} already terminated... ----")
