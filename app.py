import streamlit as st
import os
import logging
import time
from command import send_worker_command, server_run_check, delete_csv
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
run_check = str(os.getenv('RUNC', default=None))


session = st.session_state
if "choice" not in session:
    session["choice"] = None
if "datacsv" not in session:
    session["datacsv"] = str(os.getenv('BCSV', default=None))


def update_choice(choice: str | None = None):
    session["choice"] = choice

# def run_server():
#    ctx = get_script_run_ctx()
#    server = Popen(["python", "./server/server.py",
#                   '-c', f'{session.get("choice")}'])
#    session["process_id"] = server.pid
#    add_script_run_ctx(server, ctx)


# def run_home_page():
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
    server_run_check()
    delete_csv()
    send_worker_command(
        command=f'nohup python /server/server.py -c {session.get("choice")}')
    time.sleep(.25)
    st.switch_page("pages/page_2.py")
