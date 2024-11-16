import importlib
import streamlit as st
import os
import psutil
import signal
import time
from subprocess import Popen
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
utils = importlib.import_module('utils')

session = st.session_state
if "choice" not in session:
    session["choice"] = None
if "process_id" not in session:
    session["process_id"] = None
if "datacsv" not in session:
    session["datacsv"] = str(os.getenv('BCSV', default=None))


process_id = session.get("process_id")
if process_id != None and psutil.pid_exists(int(process_id)):
    utils.server_pid_terminate(process_id)

if os.path.isfile(session.get("datacsv")) == True:
    os.remove(session.get("datacsv"))

st.set_page_config(
    page_title="About this Demo", layout="centered")

st.subheader(body="About this Websocket Application")
st.text_area(height=210, label='label',
             value='This websocket demo application displays live volume data from Binance, via the Finnhub API, for your selected cryptocurrency.'
             ' A call is made to the API every 2 seconds, the data is processed, and presented on this moving bar chart.'
             ' The y-axis represents the trade volume, and the x-axis represents the time at which trade(s) occurred.'
             ' The timestamps are in ascending order from right to left.'
             ' Data collection occurs for 3 minutes, and ceases upon reaching the time limit.',
             label_visibility="collapsed")


choice = st.selectbox("See live data for one of the following options:",
                      ("Bitcoin", "Ethereum", "Dogecoin"))


def update_choice():
    session["choice"] = choice


next_button = st.button("Next", on_click=update_choice)
if next_button:
    open(session.get("datacsv"), "x")

    ctx = get_script_run_ctx()
    server = Popen(["python", "server.py", '-c', f'{session.get("choice")}'])
    session["process_id"] = server.pid
    add_script_run_ctx(server, ctx)

    st.switch_page("pages/page_2.py")
