import logging
import paramiko
from get_docker_secret import get_docker_secret
import os
import base64
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
run_check = str(os.getenv('RUNC', default=None))
filepath = str(os.getenv('BCSV', default=None))

inputs = get_docker_secret("input")
inputs_list = inputs.split("&X4")
decoded_inputs = []
for item in inputs_list:
    base64_bytes = item.encode("ascii")
    secret_bytes = base64.b64decode(base64_bytes)
    decoded_item = secret_bytes.decode("ascii")
    decoded_inputs.append(decoded_item)

strmltpwde = get_docker_secret("streamlit")
base64_bytes = strmltpwde.encode("ascii")
secret_bytes = base64.b64decode(base64_bytes)
strmltpwd = secret_bytes.decode("ascii")


def send_worker_command(command: str | None = None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cmd_list = command.split()
    ssh.connect(hostname=decoded_inputs[0], port=22,
                username=decoded_inputs[1], password=strmltpwd)
    stdin, stdout, stderr = ssh.exec_command(command=command)
    if "nohup" not in cmd_list:
        errors = stderr.read().decode('utf-8').strip()
        logger.info(
            f' Command Status: {errors if errors else "No errors to log."}')
    ssh.close()
    logger.info(" Command sent. SSH closed.")
    return


def delete_csv():
    if os.path.exists(filepath) == True:
        logger.info(" Deleting csv file...")
        send_worker_command(
            command="rm /server/data/data.csv")
    elif os.path.exists(filepath) == False:
        logger.info(f' No csv file to delete.')


def server_run_check():
    try:
        run_check_file = open(run_check, "r")
        if os.path.exists(run_check) == True:
            if run_check_file.read() == "on":
                logger.info(" Server is still running. Shutting down now...")
                send_worker_command(
                    command="python /server/utils.py -f search -fa /server/server.py")
            if run_check_file.read() == "off":
                logger.info(" Server has already been shut down.")
        else:
            pass
    except FileNotFoundError:
        logger.info(" No check file detected. Creating...")
