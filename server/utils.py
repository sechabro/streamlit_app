import signal
import psutil
import os
from argparse import ArgumentParser
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
run_check = str(os.getenv('RUNC', default=None))


def run_check_off():
    with open(run_check, "w") as run_check_file:
        run_check_file.write("off")
    logger.info(" Check file turned off. Server no longer running.")


def server_pid_terminate(pid):
    if psutil.pid_exists(int(pid)):
        logger.info(f" Terminating server script process id {pid}.")
        os.kill(int(pid), signal.SIGTERM)
    else:
        logger.info(f"pid {pid} already terminated... ----")


def server_search_and_terminate(script=None):
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['pid', 'name', 'cmdline'])
            if script in process_info["cmdline"] and "-c" in process_info["cmdline"]:
                logger.info(" Script found...")
                pid = process_info.get("pid")
                server_pid_terminate(pid=pid)
                run_check_off()
                logger.info(" Terminated server run successfully.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, TypeError):
            continue
    return f'---- No server subprocess to terminate. Server has either already been terminated, or the app is running for the first time. ----'


def main(func=None, funcarg=None):
    if func == "search":
        server_search_and_terminate(script=funcarg)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        '-f', '--func', help='function to run is either search or pid', required=True)
    parser.add_argument(
        '-fa', '--farg', help='function-specific argument', required=True)
    args = parser.parse_args()
    func = args.func
    funcarg = args.farg
    main(func=func, funcarg=funcarg)
