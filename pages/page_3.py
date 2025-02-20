import importlib
import streamlit as st
import psutil
from command import send_worker_command, server_run_check, delete_csv
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = "https://github.com/sechabro/streamlit_app"

st.set_page_config(
    page_title=f"Live Trade Volume Data Feed - Thank You", layout="wide")
col1, col2, col3 = st.columns(
    spec=[.31, .38, .31], gap="large", vertical_alignment="bottom")
col2.header("How the App Works")
col4, col5, col6 = st.columns(
    spec=[0.15, 0.7, 0.15], gap="large", vertical_alignment="center")
col7, col8, col9 = st.columns(
    spec=[.15, .7, .15], gap="large", vertical_alignment="top")
col5.write(
    f'This is a two-container application. A web container, which displays all data, and a worker container, which serves the data. The web container uses basic auth credentials to SSH into the worker container and run commands. Below is a high-level view of the deployment infrastructure.'
)
col5.image(image="./img/app_deployment_infrastructure.png",
           caption="deployment infrastructure")
col5.write(
    f'When a user selects a currency, and clicks the `Next` button, a command is constructed, and secrets are gathered to prepare for SSH login:'
)

col5.code(
    '''inputs = get_docker_secret("input") # <-- An encoded string which is read via a file during docker compose.
inputs_list = inputs.split("&X4") # <-- Splitting the string at this block. Normally, the block should be hidden.
decoded_inputs = []
for item in inputs_list:
    base64_bytes = item.encode("ascii")
    secret_bytes = base64.b64decode(base64_bytes)
    decoded_item = secret_bytes.decode("ascii")
    decoded_inputs.append(decoded_item)

# Doing the same thing here as above.
strmltpwde = get_docker_secret("streamlit")
base64_bytes = strmltpwde.encode("ascii")
secret_bytes = base64.b64decode(base64_bytes)
strmltpwd = secret_bytes.decode("ascii")''', language="python"
)
col5.write(
    f'With the secrets split and decoded, the web container is ready to SSH into the worker container and run commands. Using the Paramiko library to do so, the function below is then called:'
)
col5.code('''def send_worker_command(command: str | None = None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # <-- Basic auth, so we prevent a missing key exception.
    cmd_list = command.split()
    ssh.connect(hostname=decoded_inputs[0], port=22,
                username=decoded_inputs[1], password=strmltpwd)
    stdin, stdout, stderr = ssh.exec_command(command=command)
          
    # The worker container is on a 3-minute timer, so we need to be able to logout of the SSH session without having
    # to wait for the process to complete. Therefore, we check if `nohup` is included in the constructed command.
    # If it's not included, we can wait for the stderr readout of the process.
    if "nohup" not in cmd_list:
        errors = stderr.read().decode('utf-8').strip()
        logger.info(
            f' Command Status: {errors if errors else "No errors to log."}')
    ssh.close()
    logger.info(" Command sent. SSH closed.")
    return''', language="python")
col5.write('To autokill worker container processes in the event of a return to the home page, a refresh of page_2, or an advance to this page, first a check is run to see if the server process is running in the worker container:')
col5.code(
    '''def server_run_check():
    try:
        # We don't want to iterate through container processes every time this check is run. So there is a check file
        # that is read first.
        run_check_file = open(run_check, "r")
        if os.path.exists(run_check) == True:
            if run_check_file.read() == "on":
                logger.info(" Server is still running. Shutting down now...")

                # Intentionally over-engineering this command. At the moment, only the server runs in the worker
                # container. However, if there are more processes to search for, here is where the process would
                # be specified.
                send_worker_command(
                    command="python /server/utils.py -f search -fa /server/server.py")
            if run_check_file.read() == "off":
                logger.info(" Server has already been shut down.")
        else:
            pass

    # If the application is being started for the first time, the function will throw an exception since the check
    # file doesn't exist yet. This is the bypass for that exception.
    except FileNotFoundError:
        logger.info(" No check file detected. Creating...")'''
)
col5.write(
    f'And finally, the following is how server process is terminated:'
)
col5.code('''def server_search_and_terminate(script=None):
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['pid', 'name', 'cmdline'])
            if script in process_info["cmdline"] and "-c" in process_info["cmdline"]:
                logger.info(" Script found...")
                pid = process_info.get("pid")
                server_pid_terminate(pid=pid)
                run_check_off()
                return # <-- If we found and terminated our worker's server process, no need to continue.
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, TypeError):
            continue
    return f'No server subprocess to terminate. Is the app running for the first time?''', language="python")
col5.write(
    "If necessary, I can go into greater detail over a call. Thanks for your time! The app's repo can be found [here](%s)" % url)
if col8.button("Home"):
    st.switch_page("app.py")
