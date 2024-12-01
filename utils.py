import signal
import psutil
import os


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
    if psutil.pid_exists(int(pid)):
        print(f"##### Killing pid {pid} #####")
        os.kill(int(pid), signal.SIGTERM)
    else:
        print(f"##### pid {pid} already terminated... #####")
