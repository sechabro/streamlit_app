import importlib
import streamlit as st
import psutil
utils = importlib.import_module('utils')

url = "https://github.com/sechabro/streamlit_app"
session = st.session_state
choice = session.get("choice")
process_id = session.get("process_id")


def kill_pid():
    if process_id != None and psutil.pid_exists(int(process_id)):
        utils.server_pid_terminate(process_id)


def run_page_3():
    st.set_page_config(
        page_title=f"Live Trade Volume Data Feed - Thank You", layout="wide")
    col1, col2, col3 = st.columns(
        spec=[.31, .38, .31], gap="large", vertical_alignment="bottom")
    col2.header("Comments and Challenges ")
    col4, col5, col6 = st.columns(
        spec=[0.15, 0.7, 0.15], gap="large", vertical_alignment="center")
    col7, col8, col9 = st.columns(
        spec=[.15, .7, .15], gap="large", vertical_alignment="top")
    col5.write(
        f'The main challenge for this application was session data management. Streamlit has the `st.session_data` object, which works perfectly when everything is contained within the Streamlit runtime. However, I have a `server.py` script that operates outside of the Streamlit runtime. This script needs access to two arguments: its own process id, and the cryptocurrency choice from the home page. This information is added as `st.session_data["process_id"]` and `st.session_data["choice"]`, respectively.')
    col5.write(
        'For `script.py` to gain access to the cryptocurrency choice, I ran it as a subprocess, and fed the choice as an argument in the run command, as shown on line 3 of the code snippet below.')
    col5.code('''def run_server():
    ctx = get_script_run_ctx()
    server = Popen(["python", "server.py", '-c', f'{session.get("choice")}'])
    session["process_id"] = server.pid
    add_script_run_ctx(server, ctx)''', language="python")
    col5.write('To autokill `server.py` in the edge case of a refresh of page 2, a utility function iterates through all processes until it finds process id for the script, and then terminates it using the process id:')
    col5.code('''
    def server_search_and_terminate(script):
        for process in psutil.process_iter():
            try:
                process_info = process.as_dict(attrs=['pid', 'name', 'cmdline'])
                if process_info["name"] == "Python" and script in process_info["cmdline"]:
                    process.send_signal(signal.SIGTERM)
                    return f'##### Killed process {process_info.get("pid")} successfully. #####'
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, TypeError):
                continue
        return f'##### Server subprocess already terminated. No PID available. #####''', language="python")
    col5.write(
        "Thanks for your time! The app's repo can be found [here](%s)" % url)
    if col8.button("Home"):
        st.switch_page("app.py")


kill_pid()
run_page_3()
