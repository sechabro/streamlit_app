from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
from subprocess import Popen
import importlib
import streamlit as st
import os
import psutil
import logging
from server.utils import server_pid_terminate, server_search_and_terminate
# from ..server import utils
logging.basicConfig(level=logging.INFO)
# utils = importlib.import_module("utils", package="server")
logger = logging.getLogger(__name__)


session = st.session_state
if "choice" not in session:
    session["choice"] = None
if "process_id" not in session:
    session["process_id"] = None
if "datacsv" not in session:
    session["datacsv"] = str(os.getenv('BCSV', default=None))


def process_and_file_reset():
    ret_val = {}
    if os.path.isfile(session.get("datacsv")) == True:
        os.remove(session.get("datacsv"))
        ret_val.update({"csv_removed": True})
    process_id = session.get("process_id")
    if process_id != None and psutil.pid_exists(int(process_id)):
        server_pid_terminate(process_id)
        ret_val.update({"pid_kill": True})
    return ret_val


def update_choice(choice: str | None = None):
    session["choice"] = choice


def run_server():
    ctx = get_script_run_ctx()
    server = Popen(["python", "./server/server.py",
                   '-c', f'{session.get("choice")}'])
    session["process_id"] = server.pid
    add_script_run_ctx(server, ctx)


def run_home_page():
    st.set_page_config(
        page_title="Live Trade Volume Data Feed - Intro", layout="centered")
    st.subheader(body="About this Websocket Application")
    st.text_area(height=210, label='label',
                 value='This websocket demo application displays live volume data from Binance, via the Finnhub API, for your selected cryptocurrency.'
                 ' A call is made to the API every 2 seconds, the data is processed, and presented on a moving bar chart.'
                 ' The y-axis represents a precise unit of time, and the x-axis represents the trade volume.'
                 ' The timestamps are in descending order, and new timestamps populate from the bottom of the chart.'
                 ' Data collection occurs for 3 minutes, and ceases upon reaching the time limit.',
                 label_visibility="collapsed")

    choice = st.selectbox("See live data for one of the following options:",
                          ("Bitcoin", "Ethereum", "Dogecoin"))

    next_button = st.button("Next", on_click=update_choice(choice=choice))
    if next_button:
        open(session.get("datacsv"), "x")
        run_server()
        st.switch_page("pages/page_2.py")


script_kill = server_search_and_terminate(script="./server/server.py")
logger.info(script_kill)
reset = process_and_file_reset()
logger.info(str(reset))
run_home_page()
